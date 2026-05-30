from django.apps import AppConfig


class AppliancesConfig(AppConfig):
    """Configuration for the appliances app (Appliance model + Factory pattern)."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appliances'
