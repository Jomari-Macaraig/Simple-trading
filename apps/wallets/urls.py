from django.urls import path

from .views import WalletRetrieveAPIView, BalanceListAPIView, BalanceRetrieveAPIView

urlpatterns = [
    path("", WalletRetrieveAPIView.as_view()),
    path("balance", BalanceListAPIView.as_view()),
    path("balance/<str:ticker>", BalanceRetrieveAPIView.as_view()),
]
