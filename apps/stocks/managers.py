from django.db.models import QuerySet


class StockQueryset(QuerySet):

    def active(self):
        return self.filter(is_active=True)