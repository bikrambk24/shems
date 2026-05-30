from django.apps import AppConfig


class EnergyConfig(AppConfig):
    """Configuration for the energy app (EnergyUsage, Notification, FaultTicket + Observer)."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'energy'
