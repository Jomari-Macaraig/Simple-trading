from rest_framework.generics import CreateAPIView, ListAPIView

from .models import Order, BulkOrder
from .serializers import OrderSerializer, OrderSummarySerializer, BuldOrderSerializer
from .tasks import process_order


class OrderCreateAPIView(CreateAPIView):
    model = Order
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        process_order.apply_async(kwargs={"order_id": serializer.instance.id})


class OrderSummaryAPI(ListAPIView):
    serializer_class = OrderSummarySerializer
    pagination_class = None

    def get_queryset(self):
        ticker = self.kwargs["ticker"]
        queryset = Order.objects.active().filter(
            user=self.request.user,
            stock__ticker=ticker,
        ).calculate_summary()
        return queryset


class BulkOrderCreateAPIView(CreateAPIView):
    model = BulkOrder
    serializer_class = BuldOrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)