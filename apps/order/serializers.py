from rest_framework import serializers

from apps.stock.models import Stock
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
