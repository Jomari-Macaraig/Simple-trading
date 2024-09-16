from django.contrib import admin
from .models import Stock


class StockAdmin(admin.ModelAdmin):
    list_display = ("ticker", "price", "is_active")
    list_editable = ("is_active",)


admin.site.register(Stock, StockAdmin)
