from django.contrib import admin

from .models import Order, BulkOrder


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "ticker", "quantity", "type", "status")
    search_fields = ("user__username",)

    def ticker(self, obj):
        return obj.stock.ticker


class BulkOrderAdmin(admin.ModelAdmin):
    list_display = ("file", "status")
    readonly_fields = ("file", "status")


admin.site.register(Order, OrderAdmin)
admin.site.register(BulkOrder, BulkOrderAdmin)
