from rest_framework.generics import ListAPIView

from .models import Stock
from .serializers import StockSerializer


class StockListAPIView(ListAPIView):
    serializer_class = StockSerializer

    def get_queryset(self):
        return Stock.objects.active()
