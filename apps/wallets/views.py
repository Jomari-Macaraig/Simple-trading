from rest_framework.generics import RetrieveAPIView

from .models import Wallet
from .serializers import WalletSerializer


class WalletRetrieveAPIView(RetrieveAPIView):
    serializer_class = WalletSerializer

    def get_object(self):
        return Wallet.objects.get(user=self.request.user)
