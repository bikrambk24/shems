from django.contrib.auth.models import AbstractUser
from django.db import models


# Extends Django's built in user to add a role field
class User(AbstractUser):

    HOMEOWNER = 'HOMEOWNER'
    ADMIN = 'ADMIN'
    TECHNICIAN = 'TECHNICIAN'

    ROLE_CHOICES = [
        (HOMEOWNER, 'Homeowner'),
        (ADMIN, 'Admin'),
        (TECHNICIAN, 'Technician'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=HOMEOWNER)

    def is_homeowner(self):
        return self.role == self.HOMEOWNER

    def is_admin_user(self):
        # Named is_admin_user to avoid shadowing Django's built in is_staff attribute
        return self.role == self.ADMIN

    def is_technician(self):
        return self.role == self.TECHNICIAN

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'


# One settings record per homeowner, auto-created at registration
class HomeownerSettings(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='homeownersettings')

    # String reference avoids a circular import with the pricing app
    pricing_plan = models.ForeignKey(
        'pricing.PricingPlan',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='homeowners',
    )

    daily_threshold_kwh = models.FloatField(default=10.0)

    def __str__(self):
        return f'Settings for {self.user.username}'
