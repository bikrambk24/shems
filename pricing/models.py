from django.db import models

from pricing.strategies import FlatRateStrategy, GreenEnergyStrategy, TimeOfUseStrategy


class PricingPlan(models.Model):

    FLAT_RATE = 'FlatRate'
    TIME_OF_USE = 'TimeOfUse'
    GREEN_ENERGY = 'GreenEnergy'

    STRATEGY_CHOICES = [
        (FLAT_RATE, 'Flat Rate'),
        (TIME_OF_USE, 'Time of Use'),
        (GREEN_ENERGY, 'Green Energy'),
    ]

    name = models.CharField(max_length=100)
    strategy_type = models.CharField(max_length=20, choices=STRATEGY_CHOICES)  # selects the billing algorithm

    base_rate = models.FloatField(help_text='Cost per kWh in pence (e.g. 28.0 = 28p/kWh).')

    # Used only by TimeOfUseStrategy
    peak_rate = models.FloatField(default=0.0, help_text='Peak-hour cost per kWh in pence.')
    peak_start_hour = models.IntegerField(default=7, help_text='Hour (0-23) when peak pricing starts.')
    peak_end_hour = models.IntegerField(default=22, help_text='Hour (0-23) when peak pricing ends.')

    # Used only by GreenEnergyStrategy
    green_discount_percent = models.FloatField(default=0.0, help_text='Percentage discount off base rate.')

    is_active = models.BooleanField(default=True, help_text='Only active plans appear in the homeowner dropdown.')

    def get_strategy(self):
        # Bridge between the database record and the Strategy pattern
        if self.strategy_type == self.FLAT_RATE:
            return FlatRateStrategy(base_rate=self.base_rate)

        elif self.strategy_type == self.TIME_OF_USE:
            return TimeOfUseStrategy(
                base_rate=self.base_rate,
                peak_rate=self.peak_rate,
                peak_start_hour=self.peak_start_hour,
                peak_end_hour=self.peak_end_hour,
            )

        elif self.strategy_type == self.GREEN_ENERGY:
            return GreenEnergyStrategy(
                base_rate=self.base_rate,
                discount_percent=self.green_discount_percent,
            )

        return FlatRateStrategy(base_rate=self.base_rate)  # fallback

    def __str__(self):
        return f'{self.name} ({self.get_strategy_type_display()})'
