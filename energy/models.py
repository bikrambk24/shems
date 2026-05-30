from django.conf import settings
from django.db import models
from django.db.models import Sum

from core.ems import EnergyManagementSystem


# Records a single energy reading for one appliance
class EnergyUsage(models.Model):

    appliance = models.ForeignKey(
        'appliances.Appliance',
        on_delete=models.CASCADE,
        related_name='usage_records',
    )
    kwh_consumed = models.FloatField()
    recorded_at = models.DateTimeField()

    class Meta:
        ordering = ['-recorded_at']

    def save(self, *args, **kwargs):
        is_new_record = self.pk is None  # True only on first save, not updates
        super().save(*args, **kwargs)

        if is_new_record:
            appliance = self.appliance
            homeowner = appliance.owner

            # Get the homeowner's daily alert limit; fall back to 10 kWh if not set yet
            try:
                daily_threshold_kwh = homeowner.homeownersettings.daily_threshold_kwh
            except Exception:
                daily_threshold_kwh = 10.0

            # Sum all readings for this homeowner on the same calendar date
            reading_date = self.recorded_at.date()
            daily_total_kwh = (
                EnergyUsage.objects
                .filter(appliance__owner=homeowner, recorded_at__date=reading_date)
                .aggregate(total=Sum('kwh_consumed'))['total']
            ) or 0.0

            # Pass computed values to EMS — EMS itself does no DB queries (Dependency Inversion)
            ems = EnergyManagementSystem()
            ems.check_thresholds(appliance, daily_total_kwh, daily_threshold_kwh)

    def __str__(self):
        return f'{self.appliance.name}: {self.kwh_consumed} kWh @ {self.recorded_at:%Y-%m-%d %H:%M}'


# In-app alert shown as a banner on the homeowner's dashboard
class Notification(models.Model):

    INFO = 'info'
    WARNING = 'warning'
    CRITICAL = 'critical'

    LEVEL_CHOICES = [
        (INFO, 'Info'),
        (WARNING, 'Warning'),
        (CRITICAL, 'Critical'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    message = models.TextField()
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default=WARNING)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.level.upper()}] {self.user.username}: {self.message[:60]}'


# Admin-only audit trail — records every threshold event even if nobody saw the banner
class NotificationLog(models.Model):

    appliance = models.ForeignKey(
        'appliances.Appliance',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notification_logs',
    )
    event_type = models.CharField(max_length=50)  # e.g. 'threshold_exceeded' or 'fault_detected'
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.event_type} at {self.created_at:%Y-%m-%d %H:%M}'


# Helpdesk-style ticket raised when an appliance may be malfunctioning
class FaultTicket(models.Model):

    OPEN = 'Open'
    IN_PROGRESS = 'InProgress'
    RESOLVED = 'Resolved'

    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (IN_PROGRESS, 'In Progress'),
        (RESOLVED, 'Resolved'),
    ]

    appliance = models.ForeignKey(
        'appliances.Appliance',
        on_delete=models.CASCADE,
        related_name='fault_tickets',
    )
    reported_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=OPEN)
    notes = models.TextField(blank=True)

    resolved_by = models.ForeignKey(  # only set when a technician closes the ticket
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_tickets',
    )

    class Meta:
        ordering = ['-reported_at']

    def __str__(self):
        return f'Ticket #{self.pk} — {self.appliance.name} [{self.status}]'
