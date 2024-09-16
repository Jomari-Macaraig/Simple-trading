from django.db import models
from django.contrib.auth.models import User

from apps.base.models import Audit, DECIMAL_MAX_DIGITS, DECIMAL_MAX_DECIMAL_PLACES
from apps.base.utils import generate_uuid
from apps.stocks.models import Stock
from .constants import WalletTransactionType, WalletTransactionStatus


class Wallet(Audit):
    uid = models.UUIDField(unique=True, default=generate_uuid, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    running_balance = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_MAX_DECIMAL_PLACES,
        default=0
    )

    def __str__(self):
        return f"{self.user.username.title()}'s Wallet"


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
    quantity = models.DecimalField(max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_MAX_DECIMAL_PLACES)