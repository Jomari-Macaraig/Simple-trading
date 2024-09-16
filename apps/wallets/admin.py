from django.contrib import admin

from .models import Wallet, WalletTransaction, Balance
from .tasks import process_wallet_transaction


class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "uid", "running_balance", "is_active")
    list_editable = ("is_active",)
    fields = ("user", "is_active")


class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ("wallet", "type", "status")
    readonly_fields = ["status",]

    def get_readonly_fields(self, request, obj=None):
        read_only_fields = list(super().get_readonly_fields(request=request, obj=obj))
        if obj:
            read_only_fields.extend(["wallet", "type", "amount"])
        return read_only_fields

    def save_model(self, request, obj, form, change):
        response = super().save_model(request=request, obj=obj, form=form, change=change)
        process_wallet_transaction.apply_async(kwargs={"wallet_transaction_id": obj.id})
        return response


class BalanceAdmin(admin.ModelAdmin):
    list_display = ("wallet", "stock", "quantity")
    readonly_fields = ("wallet", "stock", "quantity")


admin.site.register(Wallet, WalletAdmin)
admin.site.register(WalletTransaction, WalletTransactionAdmin)
admin.site.register(Balance, BalanceAdmin)
