from django.contrib import admin
from .models import DomofonCall

@admin.register(DomofonCall)
class DomofonCallAdmin(admin.ModelAdmin):
    list_display = ('apartment_number', 'mac_address', 'call_time', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('apartment_number', 'mac_address')