from django.urls import path

from .views import OrderCreateAPIView

urlpatterns = [
    path("", OrderCreateAPIView.as_view())
]
