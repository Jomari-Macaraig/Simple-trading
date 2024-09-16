from django.db.models import (
    Sum,
    F,
    Case,
    When,
    DecimalField,
)

from apps.base.managers import BaseQueryset
from .constants import OrderType


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
