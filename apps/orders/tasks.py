from config.celery import app
from django.db import transaction

from .models import Order
from .constants import OrderType, OrderStatus
from apps.wallets.exceptions import InsufficientBalance


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
