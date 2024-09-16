from django.db import models
from django.contrib.auth.models import User

from apps.base.models import Audit
from apps.stock.models import Stock

from .constants import OrderType, OrderStatus


class Order(Audit):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=32, decimal_places=8)
    type = models.CharField(max_length=4, choices=zip(OrderType.list(), OrderType.list()))
    status = models.CharField(
        max_length=16,
        choices=zip(OrderStatus.list(), OrderStatus.list()),
        default=OrderStatus.PENDING.value,
    )
    epoch = models.PositiveIntegerField()

    class Meta:
        unique_together = ("stock", "user", "epoch")

    def __str__(self):
        return f"{self.user.username}#{self.type}#{self.stock}#{self.epoch}"
