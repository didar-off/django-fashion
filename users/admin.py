from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users import models as users_models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


@admin.register(users_models.User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'is_active', 'is_staff', 'is_vendor', 'date_joined_display')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_vendor', 'date_joined')
    search_fields = ('email', 'full_name')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'updated_at', 'image_preview')
    filter_horizontal = ('groups', 'user_permissions',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'image', 'image_preview', 'is_vendor')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('date_joined', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'is_vendor', 'password1', 'password2'),
        }),
    )

    def date_joined_display(self, obj):
        return obj.date_joined.strftime("%Y-%m-%d %H:%M")
    date_joined_display.short_description = _('Date joined')
    date_joined_display.admin_order_field = 'date_joined'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return _("No image")
    image_preview.short_description = _('Image Preview')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.is_vendor and not hasattr(obj, 'vendor'):
            from vendors.models import Vendor
            Vendor.objects.get_or_create(
                user=obj,
                defaults={'store_name': f"{obj.full_name}'s Store"}
            )