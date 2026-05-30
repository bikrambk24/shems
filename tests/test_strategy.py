"""
tests/test_strategy.py — Tests for the Strategy Pattern (pricing/strategies.py)

Three tests, one per concrete strategy, proving that each algorithm produces
the correct result for a known input.  All three share the same interface
(calculate(usage_kwh, timestamp)) but apply different billing logic.

No database needed — strategies are plain Python objects.
"""

import pytest
from datetime import datetime, timezone

from pricing.strategies import FlatRateStrategy, GreenEnergyStrategy, TimeOfUseStrategy


def at_hour(hour):
    """Return a timezone-aware datetime at the given hour (used to simulate peak/off-peak)."""
    return datetime(2024, 6, 15, hour, 0, 0, tzinfo=timezone.utc)


class TestStrategies:

    def test_flat_rate_returns_usage_times_rate(self):
        """
        FlatRate: cost = usage_kwh × base_rate, regardless of time of day.

        30p/kWh × 10 kWh = 300p.  The timestamp is irrelevant for this strategy.
        """
        strategy = FlatRateStrategy(base_rate=30.0)

        cost = strategy.calculate(usage_kwh=10.0, timestamp=at_hour(14))

        assert cost == pytest.approx(300.0)

    def test_time_of_use_charges_peak_rate_during_peak_hours(self):
        """
        TimeOfUse: usage at peak hours (here 5pm) costs more than the same
        usage at off-peak hours (here 2am).

        Same 10 kWh, same appliance, different time → different bill.
        This is the whole motivation for the time-of-use tariff.
        """
        strategy = TimeOfUseStrategy(
            base_rate=15.0,
            peak_rate=35.0,
            peak_start_hour=7,
            peak_end_hour=22,
        )

        peak_cost = strategy.calculate(usage_kwh=10.0, timestamp=at_hour(17))    # 5pm
        off_peak_cost = strategy.calculate(usage_kwh=10.0, timestamp=at_hour(2))  # 2am

        assert peak_cost > off_peak_cost
        assert peak_cost == pytest.approx(350.0)   # 10 kWh × 35p
        assert off_peak_cost == pytest.approx(150.0)  # 10 kWh × 15p

    def test_green_energy_applies_discount(self):
        """
        GreenEnergy: the discounted bill is lower than the undiscounted bill
        by exactly the discount percentage.

        'Without solar' (0% discount) gives the full cost.
        'With solar'    (10% discount) gives 90% of the full cost.
        The difference must be exactly 10%.
        """
        usage_kwh = 10.0
        ts = at_hour(12)

        full_cost = GreenEnergyStrategy(base_rate=30.0, discount_percent=0.0).calculate(usage_kwh, ts)
        discounted = GreenEnergyStrategy(base_rate=30.0, discount_percent=10.0).calculate(usage_kwh, ts)

        assert discounted < full_cost
        assert discounted == pytest.approx(full_cost * 0.90)  # Exactly 10% off
