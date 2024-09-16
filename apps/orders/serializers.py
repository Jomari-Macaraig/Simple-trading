from rest_framework import serializers

from apps.base.models import DECIMAL_MAX_DIGITS, DECIMAL_MAX_DECIMAL_PLACES
from apps.stocks.models import Stock
from apps.wallets.exceptions import InsufficientBalance
from apps.wallets.models import Wallet
from .constants import OrderType
from .models import Order


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
        ticker = attrs.pop("ticker")
        try:
            stock = Stock.objects.active().get(ticker=ticker)
        except Stock.DoesNotExist:
            raise serializers.ValidationError({"ticker": "This ticker does not exist"})

        attrs["stock"] = stock

        try:
            wallet = self.context["request"].user.wallet
        except Wallet.DoesNotExist:
            raise serializers.ValidationError({"wallet": "User has no wallet"})

        try:
            wallet.check_balance(
                stock=stock,
                order_type=OrderType.BUY if attrs["type"] == OrderType.BUY.value else OrderType.SELL,
                quantity=attrs["quantity"],
            )
        except InsufficientBalance:
            raise serializers.ValidationError({"ticker": "Insufficient Balance"})

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