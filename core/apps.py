from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from core.ems import EnergyManagementSystem
        from energy.observers import DashboardNotifier, UsageLogger

        ems = EnergyManagementSystem()

        # Guard so ready() being called twice (e.g. during tests) doesn't attach duplicates
        if not ems.observers_attached:
            ems.attach(DashboardNotifier())
            ems.attach(UsageLogger())
            ems.observers_attached = True
