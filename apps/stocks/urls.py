from django.urls import path

from .views import StockListAPIView

urlpatterns = [
    path("", StockListAPIView.as_view())
]
