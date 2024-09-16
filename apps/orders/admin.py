from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "ticker", "quantity", "type", "status")
    search_fields = ("user__username",)

    def ticker(self, obj):
        return obj.stock.ticker


admin.site.register(Order, OrderAdmin)
