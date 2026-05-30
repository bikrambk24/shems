from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuration for the accounts app (custom User model + auth)."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
