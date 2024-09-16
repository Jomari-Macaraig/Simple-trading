from decimal import Decimal
from typing import Union

from django.contrib.auth.models import User
from django.db import models

from apps.base.models import Audit, DECIMAL_MAX_DIGITS, DECIMAL_MAX_DECIMAL_PLACES
from apps.base.utils import generate_uuid
from apps.orders.constants import OrderType
from apps.stocks.models import Stock
from .constants import WalletTransactionType, WalletTransactionStatus
from .exceptions import InsufficientBalance
from .managers import BalanceQueryset, WalletQueryset


class Wallet(Audit):
    uid = models.UUIDField(unique=True, default=generate_uuid, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    running_balance = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_MAX_DECIMAL_PLACES,
        default=0
    )

    objects = WalletQueryset.as_manager()

    def check_balance(self, stock: Stock, order_type: OrderType, quantity: Union[Decimal, str]) -> None:
        quantity = Decimal(quantity)
        if order_type == OrderType.BUY:
            stock_value = stock.price * quantity
            if stock_value > self.running_balance:
                raise InsufficientBalance(f"User has insufficient running balance")
        else:
            try:
                balance = self.balance_set.get(stock=stock)
            except Balance.DoesNotExist:
                raise InsufficientBalance(f"User has insufficient stock balance")

            if quantity > balance.quantity:
                raise InsufficientBalance(f"User has insufficient stock balance")

    def __str__(self):
        return f"{self.uid}"


class WalletTransaction(Audit):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=zip(WalletTransactionType.list(), WalletTransactionType.list()))
    amount = models.DecimalField(max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_MAX_DECIMAL_PLACES)
    status = models.CharField(
        max_length=18,
        choices=zip(WalletTransactionStatus.list(), WalletTransactionStatus.list()),
        default=WalletTransactionStatus.PENDING.value,
    )


class Balance(Audit):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_MAX_DECIMAL_PLACES,
        default=0
    )

    objects = BalanceQueryset.as_manager()

    class Meta:
        unique_together = ("wallet", "stock")

    def __str__(self):
        return f"{self.wallet}#{self.stock}#{self.quantity}"