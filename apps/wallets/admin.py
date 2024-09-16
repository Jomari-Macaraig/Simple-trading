from django.contrib import admin

from .models import Wallet, WalletTransaction, Balance
from .constants import WalletTransactionStatus


class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "uid", "running_balance")


class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ("wallet", "type", "status")

    def get_readonly_fields(self, request, obj=None):
        read_only_fields = list(super().get_readonly_fields(request=request, obj=obj))
        if not obj or (obj and obj.status == WalletTransactionStatus.COMPLETED.value):
            read_only_fields.append("status")
        if obj:
            read_only_fields.extend(["wallet", "type", "amount"])
        return read_only_fields


admin.site.register(Wallet, WalletAdmin)
admin.site.register(WalletTransaction, WalletTransactionAdmin)
