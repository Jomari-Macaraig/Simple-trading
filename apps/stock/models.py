from django.db import models

from apps.base.models import Audit

from .managers import StockQueryset


class Stock(Audit):
    ticker = models.CharField(max_length=16, unique=True)
    price = models.DecimalField(max_digits=32, decimal_places=8)

    objects = StockQueryset.as_manager()

    def __str__(self):
        return self.ticker
