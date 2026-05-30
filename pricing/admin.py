from django.contrib import admin

from pricing.models import PricingPlan


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'strategy_type', 'base_rate', 'is_active']
    list_filter = ['strategy_type', 'is_active']
