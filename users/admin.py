from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from users import models as users_models


@admin.register(users_models.User)
class UserAdmin(BaseUserAdmin):
    ordering = ['-date_joined']
    list_display = ('email', 'full_name', 'user_type', 'is_vendor_verified', 'is_active', 'is_staff')
    list_filter = ('user_type', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'full_name')
    readonly_fields = ('date_joined', 'updated_at')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': ('full_name', 'image', 'user_type')
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        (_('Important dates'), {
            'fields': ('date_joined', 'updated_at')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'full_name', 'user_type',
                'image', 'password1', 'password2',
                'is_active', 'is_staff', 'is_superuser'
            ),
        }),
    )