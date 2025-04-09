from django.contrib import admin
from vendors import models as vendors_models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


@admin.register(vendors_models.Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = (
        'store_name', 'user_email', 'is_verified',
        'store_logo_preview', 'created_at'
    )
    list_filter = ('is_verified', 'created_at')
    search_fields = ('store_name', 'user__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'store_logo_preview')

    fieldsets = (
        (None, {
            'fields': (
                'user', 'store_name', 'description',
                'store_logo', 'store_logo_preview',
                'is_verified', 'created_at'
            )
        }),
    )

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = _('User Email')

    def store_logo_preview(self, obj):
        if obj.store_logo:
            return format_html(
                '<img src="{}" style="height: 50px; border-radius: 4px;" />',
                obj.store_logo.url
            )
        return "-"
    store_logo_preview.short_description = _('Logo Preview')