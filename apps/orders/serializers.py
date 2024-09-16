from rest_framework import serializers

from apps.base.models import DECIMAL_MAX_DIGITS, DECIMAL_MAX_DECIMAL_PLACES
from apps.stocks.exceptions import TickerNotFound
from apps.stocks.models import Stock
from apps.wallets.exceptions import InsufficientBalance
from apps.wallets.exceptions import WalletNotFound
from .exceptions import OrderTypeNotFound
from .models import Order, BulkOrder


class OrderSerializer(serializers.ModelSerializer):
    ticker = serializers.CharField(write_only=True)

    class Meta:
        model = Order
        fields = (
            "quantity",
            "type",
            "epoch",
            "ticker",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance=instance)
        representation["ticker"] = instance.stock.ticker
        return representation

    def validate(self, attrs):
        super().validate(attrs=attrs)
        try:
            Order.objects.validate_order(user=self.context["request"].user, data=attrs)
        except TickerNotFound:
            raise serializers.ValidationError({"ticker": "This ticker does not exist."})
        except WalletNotFound:
            raise serializers.ValidationError({"wallet": "User has no wallet."})
        except InsufficientBalance:
            raise serializers.ValidationError({"ticker": "Insufficient Balance."})
        except OrderTypeNotFound:
            raise serializers.ValidationError({"type": "Invalid order type."})

        ticker = attrs.pop("ticker")
        attrs["stock"] = Stock.objects.active().get(ticker=ticker)

        return attrs


class OrderSummarySerializer(serializers.Serializer):
    status = serializers.CharField(read_only=True)
    total_quantity = serializers.DecimalField(
        read_only=True,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_MAX_DECIMAL_PLACES
    )
    total_value = serializers.DecimalField(
        read_only=True,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_MAX_DECIMAL_PLACES
    )


class BuldOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = BulkOrder
        fields = ("file",)