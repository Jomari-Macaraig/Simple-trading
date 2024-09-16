from decimal import Decimal

from apps.base.managers import BaseQueryset
from apps.stocks.models import Stock


class WalletQueryset(BaseQueryset):
    pass


class BalanceQueryset(BaseQueryset):

    def create_or_update(self, wallet, stock: Stock, quantity: Decimal):
        try:
            balance = self.model.objects.get(wallet=wallet, stock=stock)
        except self.model.DoesNotExist:
            balance = self.model.objects.create(wallet=wallet, stock=stock)

        balance.quantity += quantity
        balance.save()
        return balance