from django.db import models

from apps.base.models import Audit, DECIMAL_MAX_DIGITS, DECIMAL_MAX_DECIMAL_PLACES

from .managers import StockQueryset


class Stock(Audit):
    ticker = models.CharField(max_length=16, unique=True)
    price = models.DecimalField(max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_MAX_DECIMAL_PLACES)

    objects = StockQueryset.as_manager()

    def __str__(self):
        return self.ticker
