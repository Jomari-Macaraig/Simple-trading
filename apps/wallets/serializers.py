from rest_framework import serializers

from . models import Wallet, Balance


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ("uid", "running_balance")


class BalanceSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    stock = serializers.StringRelatedField()

    class Meta:
        model = Balance
        fields = ("stock", "amount")

    def get_amount(self, obj):
        return obj.quantity * obj.stock.price