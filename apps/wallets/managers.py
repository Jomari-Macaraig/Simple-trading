from decimal import Decimal

from django.db.models import QuerySet

from apps.stocks.models import Stock


class BalanceQueryset(QuerySet):

    def create_or_update(self, wallet, stock: Stock, quantity: Decimal):
        try:
            balance = self.model.objects.get(wallet=wallet, stock=stock)
        except self.model.DoesNotExist:
            balance = self.model.objects.create(wallet=wallet, stock=stock)

        balance.quantity += quantity
        balance.save()
        return balance