from typing import Dict

from django.contrib.auth.models import User
from django.db.models import (
    Sum,
    F,
    Case,
    When,
    DecimalField,
)

from apps.base.managers import BaseQueryset
from apps.stocks.exceptions import TickerNotFound
from apps.stocks.models import Stock
from apps.wallets.exceptions import WalletNotFound
from apps.wallets.models import Wallet
from .constants import OrderType
from .exceptions import OrderTypeNotFound


class OrderQueryset(BaseQueryset):

    def calculate_summary(self):
        queryset = self.values("status").annotate(
            total_buy_quantity=Sum(
                Case(
                    When(type=OrderType.BUY.value, then=F("quantity")),
                    default=0,
                    output_field=DecimalField(),
                )
            ),
            total_sell_quantity=Sum(
                Case(
                    When(type=OrderType.SELL.value, then=F("quantity")),
                    default=0,
                    output_field=DecimalField(),
                )
            ),
            total_quantity=F("total_buy_quantity") - F("total_sell_quantity"),
            total_value=F("total_quantity") * F("stock__price")
        )
        return queryset

    def validate_order(self, user: User, data: Dict):
        ticker = data["ticker"]
        order_type = data["type"]
        try:
            stock = Stock.objects.active().get(ticker=ticker)
        except Stock.DoesNotExist:
            raise TickerNotFound(f"Stock with {ticker} not found.")

        try:
            wallet = user.wallet
        except Wallet.DoesNotExist:
            raise WalletNotFound(f"User {user} has no wallet.")

        if order_type not in OrderType.list():
            raise OrderTypeNotFound(f"Order type {order_type} not found.")

        wallet.check_balance(
            stock=stock,
            order_type=OrderType.BUY if order_type == OrderType.BUY.value else OrderType.SELL,
            quantity=data["quantity"],
        )


class BulkOrderQueryset(BaseQueryset):
    pass
