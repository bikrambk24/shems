from django.conf import settings
from django.db import models


class Appliance(models.Model):
    AC = 'AC'
    FRIDGE = 'FRIDGE'
    LIGHT = 'LIGHT'
    WASHING_MACHINE = 'WASHING_MACHINE'
    WATER_HEATER = 'WATER_HEATER'
    TV = 'TV'

    TYPE_CHOICES = [
        (AC, 'Air Conditioner'),
        (FRIDGE, 'Fridge'),
        (LIGHT, 'Light'),
        (WASHING_MACHINE, 'Washing Machine'),
        (WATER_HEATER, 'Water Heater'),
        (TV, 'Television'),
    ]
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appliances',
    )
    name = models.CharField(
        max_length=100,
        help_text='Friendly label, e.g. "Kitchen Fridge" or "Bedroom AC".',
    )
    appliance_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    power_rating_kw = models.FloatField(
        help_text='Manufacturer-rated power draw in kilowatts (e.g. 1.5 for a typical AC).',
    )
    is_on = models.BooleanField(default=False)
    is_faulty = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = 'ON' if self.is_on else 'OFF'
        return f'{self.name} ({self.get_appliance_type_display()}) — {status}'
