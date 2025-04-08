from django.contrib import admin
from vendors.models import Vendor
from django.utils.translation import gettext_lazy as _


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'user', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('store_name', 'user__email')
