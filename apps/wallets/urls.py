from django.urls import path

from .views import WalletRetrieveAPIView

urlpatterns = [
    path("", WalletRetrieveAPIView.as_view())
]
