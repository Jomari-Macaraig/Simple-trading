from django.urls import path

from .views import OrderCreateAPIView, OrderSummaryAPI, BulkOrderCreateAPIView

urlpatterns = [
    path("", OrderCreateAPIView.as_view()),
    path("upload/<str:filename>", BulkOrderCreateAPIView.as_view()),
    path("summary/<str:ticker>", OrderSummaryAPI.as_view()),
]
