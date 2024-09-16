from django.db.models import QuerySet


class BaseQueryset(QuerySet):

    def active(self):
        return self.filter(is_active=True)