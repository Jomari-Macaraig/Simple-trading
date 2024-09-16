from django.contrib.auth.models import User
from django.db import models

from apps.base.models import Audit, DECIMAL_MAX_DIGITS, DECIMAL_MAX_DECIMAL_PLACES
from apps.base.utils import generate_uuid
from apps.stocks.models import Stock
from .constants import OrderType, OrderStatus, BulkOrderStatus
from .managers import OrderQueryset, BulkOrderQueryset


class Order(Audit):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_MAX_DECIMAL_PLACES)
    type = models.CharField(max_length=4, choices=zip(OrderType.list(), OrderType.list()))
    status = models.CharField(
        max_length=17,
        choices=zip(OrderStatus.list(), OrderStatus.list()),
        default=OrderStatus.PENDING.value,
    )
    epoch = models.PositiveIntegerField()

    objects = OrderQueryset.as_manager()

    class Meta:
        unique_together = ("stock", "user", "epoch")

    def __str__(self):
        return f"{self.user.username}#{self.type}#{self.stock}#{self.epoch}"


class BulkOrder(Audit):
    uid = models.UUIDField(unique=True, default=generate_uuid, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/")
    status = models.CharField(
        max_length=17,
        choices=zip(BulkOrderStatus.list(), BulkOrderStatus.list()),
        default=BulkOrderStatus.PENDING.value,
    )
    remarks = models.CharField(max_length=128)
    orders = models.ManyToManyField(Order, through="BulkOrderToOrder")

    objects = BulkOrderQueryset.as_manager()

    def __str__(self):
        return f"{self.file.name}"


class BulkOrderToOrder(Audit):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    bulk_order = models.ForeignKey(BulkOrder, on_delete=models.CASCADE)