from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView, ListAPIView

from .models import Wallet, Balance
from .serializers import WalletSerializer, BalanceSerializer


class WalletRetrieveAPIView(RetrieveAPIView):
    serializer_class = WalletSerializer

    def get_queryset(self):
        return Wallet.objects.active()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            **{
                "user": self.request.user
            }
        )
        self.check_object_permissions(self.request, obj)
        return obj


class BalanceRetrieveAPIView(RetrieveAPIView):
    serializer_class = BalanceSerializer

    def get_queryset(self):
        return Balance.objects.active()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            **{
                "stock__ticker": self.kwargs["ticker"],
                "wallet__user": self.request.user
            }
        )
        self.check_object_permissions(self.request, obj)
        return obj


class BalanceListAPIView(ListAPIView):
    serializer_class = BalanceSerializer

    def get_queryset(self):
        return Balance.objects.active()