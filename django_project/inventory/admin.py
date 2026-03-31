from django.contrib import admin
from .models import Asset

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('code', 'turkish_name', 'campus', 'room', 'category', 'status', 'date')
    search_fields = ('code', 'internal_code', 'turkish_name', 'inventory_item', 'room', 'campus')
    list_filter = ('campus', 'category', 'status')
