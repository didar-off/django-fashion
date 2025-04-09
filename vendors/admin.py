from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from vendors import models as vendors_models


@admin.register(vendors_models.Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = (
        'store_name', 'user_email', 'is_verified', 'verified_at', 'preview_logo', 'rating', 'created_at'
    )
    list_filter = ('is_verified', 'created_at')
    search_fields = ('store_name', 'user__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'preview_logo', 'verified_at')

    fieldsets = (
        (None, {
            'fields': (
                'user', 'store_name', 'description', 'store_logo', 'preview_logo',
                'phone', 'website'
            )
        }),
        (_('Verification'), {
            'fields': ('is_verified', 'verified_at')
        }),
        (_('Statistics'), {
            'fields': ('rating',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = _('User Email')

    def preview_logo(self, obj):
        if obj.store_logo:
            return format_html(
                '<img src="{}" style="height: 50px; border-radius: 4px;" />',
                obj.store_logo.url
            )
        return "-"
    preview_logo.short_description = _('Logo Preview')