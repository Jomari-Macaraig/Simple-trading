import csv
from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.stocks.exceptions import TickerNotFound
from apps.stocks.models import Stock
from apps.wallets.exceptions import InsufficientBalance, WalletNotFound
from config.celery import app
from .constants import OrderType, OrderStatus, BulkOrderStatus
from .models import Order, BulkOrder


@app.task(name="order.process_order")
@transaction.atomic
def process_order(order_id: int):
    order = Order.objects.get(pk=order_id)

    if order.status == OrderStatus.PENDING.value:
        order_type = OrderType.BUY if order.type == OrderType.BUY.value else OrderType.SELL
        wallet = order.user.wallet
        try:
            wallet.check_balance(
                stock=order.stock,
                order_type=order_type,
                quantity=order.quantity,
            )
        except InsufficientBalance:
            order.status = OrderStatus.INSUFFICIENT_FUND.value
            order.save()
            return

        if order_type == OrderType.BUY:
            balance = -(order.quantity * order.stock.price)
            order_quantity = order.quantity
        else:
            balance = order.quantity * order.stock.price
            order_quantity = -order.quantity

        wallet.running_balance += balance
        wallet.balance_set.create_or_update(
            stock=order.stock,
            quantity=order_quantity,
            wallet=wallet,
        )

        order.status = OrderStatus.COMPLETED.value

        order.save()
        wallet.save()


@app.task(name="order.process_bulk_orders")
@transaction.atomic
def process_bulk_orders():
    for bulk_order in BulkOrder.objects.active().filter(status=BulkOrderStatus.PENDING.value).iterator():
        process_bulk_order.apply_async(kwargs={"bulk_order_id": bulk_order.id})


@app.task(name="order.process_bulk_order")
@transaction.atomic
def process_bulk_order(bulk_order_id: int):
    bulk_order = BulkOrder.objects.get(pk=bulk_order_id)
    if bulk_order.status == BulkOrderStatus.PENDING.value:
        user = bulk_order.user
        epoch = timezone.now().timestamp()
        orders = []
        try:
            with open(bulk_order.file.path, "r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    Order.objects.validate_order(user=bulk_order.user, data=row)
                    stock = Stock.objects.active().get(ticker=row["ticker"])
                    orders.append({
                        "stock": stock,
                        "amount": stock.price * Decimal(row["quantity"]),
                        **row
                    })
            total_amount = sum([order["amount"] for order in orders if order["type"] == OrderType.BUY.value])
            if total_amount > user.wallet.running_balance:
                raise InsufficientBalance(f"User has insufficient running balance")
        except (KeyError, TickerNotFound, WalletNotFound, InsufficientBalance) as err:
            bulk_order.status = BulkOrderStatus.FAILED.value
            bulk_order.remarks = repr(err)
            bulk_order.save()
            return

        for order_data in orders:
            order = Order.objects.create(
                stock=order_data["stock"],
                user=user,
                quantity=order_data["quantity"],
                type=order_data["type"],
                epoch=epoch,
            )
            bulk_order.orders.add(order)
        bulk_order.status = BulkOrderStatus.COMPLETED.value
        bulk_order.save()
