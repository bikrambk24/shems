from core.patterns import Observer
from energy.models import Notification, NotificationLog


# Observer 1 — creates a warning banner for the homeowner when daily limit is exceeded
class DashboardNotifier(Observer):

    def update(self, event_data):
        homeowner = event_data['homeowner']
        message = (
            f"Daily usage alert: you have used {event_data['daily_total']:.2f} kWh today, "
            f"exceeding your {event_data['daily_threshold']} kWh limit."
        )
        Notification.objects.create(user=homeowner, message=message, level=Notification.WARNING)


# Observer 2 — writes an audit log entry visible to admins
class UsageLogger(Observer):

    def update(self, event_data):
        appliance = event_data['appliance']
        details = (
            f"Appliance: {appliance.name} | "
            f"Owner: {event_data['homeowner'].username} | "
            f"Daily total: {event_data['daily_total']:.2f} kWh | "
            f"Threshold: {event_data['daily_threshold']} kWh"
        )
        NotificationLog.objects.create(
            appliance=appliance,
            event_type='threshold_exceeded',
            details=details,
        )
