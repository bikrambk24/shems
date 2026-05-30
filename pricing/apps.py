from django.apps import AppConfig


class PricingConfig(AppConfig):
    """Configuration for the pricing app (PricingPlan model + Strategy pattern)."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pricing'
