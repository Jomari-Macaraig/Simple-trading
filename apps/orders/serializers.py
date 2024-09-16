from rest_framework import serializers

from apps.base.models import DECIMAL_MAX_DIGITS, DECIMAL_MAX_DECIMAL_PLACES
from apps.stocks.models import Stock
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

    def create(self, validated_data):
        ticker = validated_data.pop("ticker")
        try:
            stock = Stock.objects.active().get(ticker=ticker)
        except Stock.DoesNotExist:
            raise serializers.ValidationError({"ticker": "This ticker does not exist"})
        return Order.objects.create(stock=stock, **validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance=instance)
        representation["ticker"] = instance.stock.ticker
        return representation


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