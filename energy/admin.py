from django.contrib import admin

from energy.models import EnergyUsage, FaultTicket, Notification, NotificationLog


@admin.register(EnergyUsage)
class EnergyUsageAdmin(admin.ModelAdmin):
    list_display = ['appliance', 'kwh_consumed', 'recorded_at']
    list_filter = ['appliance__appliance_type']
    date_hierarchy = 'recorded_at'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'message', 'created_at', 'is_read']
    list_filter = ['level', 'is_read']


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ['event_type', 'appliance', 'created_at']
    list_filter = ['event_type']


@admin.register(FaultTicket)
class FaultTicketAdmin(admin.ModelAdmin):
    list_display = ['appliance', 'status', 'reported_at', 'resolved_by']
    list_filter = ['status']
