from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User, HomeownerSettings


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Extend Django's built-in UserAdmin to display and filter by role."""
    list_display = ['username', 'email', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active']
    # Add the role field to the existing UserAdmin fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('SHEMS Role', {'fields': ('role',)}),
    )


@admin.register(HomeownerSettings)
class HomeownerSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'pricing_plan', 'daily_threshold_kwh']
