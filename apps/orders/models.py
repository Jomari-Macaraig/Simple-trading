from django.db import models
from django.contrib.auth.models import User

from apps.base.models import Audit, DECIMAL_MAX_DIGITS, DECIMAL_MAX_DECIMAL_PLACES
from apps.stocks.models import Stock

from .constants import OrderType, OrderStatus
from .managers import OrderQueryset


class Order(Audit):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_MAX_DECIMAL_PLACES)
    type = models.CharField(max_length=4, choices=zip(OrderType.list(), OrderType.list()))
    status = models.CharField(
        max_length=16,
        choices=zip(OrderStatus.list(), OrderStatus.list()),
        default=OrderStatus.PENDING.value,
    )
    epoch = models.PositiveIntegerField()

    objects = OrderQueryset.as_manager()

    class Meta:
        unique_together = ("stock", "user", "epoch")

    def __str__(self):
        return f"{self.user.username}#{self.type}#{self.stock}#{self.epoch}"
