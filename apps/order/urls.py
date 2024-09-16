from django.urls import path

from .views import OrderCreateAPIView, OrderSummaryAPI

urlpatterns = [
    path("", OrderCreateAPIView.as_view()),
    path("summary/<str:ticker>", OrderSummaryAPI.as_view()),
]
