from django.contrib import admin

from .models import Order, BulkOrder, BulkOrderToOrder


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "ticker", "quantity", "type", "status")
    search_fields = ("user__username",)

    def ticker(self, obj):
        return obj.stock.ticker


class BulkOrderAdmin(admin.ModelAdmin):
    list_display = ("uid", "file", "remarks", "status")
    readonly_fields = ("uid", "file", "remarks", )


class BulkOrderToOrderAdmin(admin.ModelAdmin):
    list_display = ("order", "bulk_order")
    readonly_fields = ("order", "bulk_order")


admin.site.register(Order, OrderAdmin)
admin.site.register(BulkOrder, BulkOrderAdmin)
admin.site.register(BulkOrderToOrder, BulkOrderToOrderAdmin)
