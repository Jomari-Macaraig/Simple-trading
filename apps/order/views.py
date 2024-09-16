from rest_framework.generics import CreateAPIView

from .models import Order
from .serializers import OrderSerializer


class OrderCreateAPIView(CreateAPIView):
    model = Order
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
