"""
tests/test_factory.py — Tests for the Factory Pattern (appliances/factories.py)

Three tests that prove the factory does its job:
  - stamps the correct appliance type on every object it builds
  - looks up the right default power rating from its DEFAULTS catalogue
  - lets the caller override any default without touching the factory code

No database is needed — the factory returns an unsaved Appliance instance
(pk is None), so these are pure in-memory unit tests.
"""

from appliances.factories import ApplianceFactory
from appliances.models import Appliance


class TestApplianceFactory:

    def test_factory_creates_correct_appliance_type(self):
        """
        The factory stamps appliance_type to match the key that was requested.
        An 'AC' request must return an object whose appliance_type is 'AC',
        not FRIDGE or any other type.
        """
        ac = ApplianceFactory.create(Appliance.AC, name='Test AC')
        assert ac.appliance_type == Appliance.AC

        fridge = ApplianceFactory.create(Appliance.FRIDGE, name='Test Fridge')
        assert fridge.appliance_type == Appliance.FRIDGE

    def test_factory_applies_correct_default_power_ratings(self):
        """
        The DEFAULTS dictionary in ApplianceFactory holds the correct rated
        power for each appliance type.  Changing a default means editing
        exactly one entry in that dictionary — not hunting across the codebase.

        AC:     1.5 kW  (typical UK split-unit air conditioner)
        FRIDGE: 0.1 kW  (energy-efficient modern unit)
        """
        ac = ApplianceFactory.create(Appliance.AC, name='AC')
        assert ac.power_rating_kw == 1.5

        fridge = ApplianceFactory.create(Appliance.FRIDGE, name='Fridge')
        assert fridge.power_rating_kw == 0.1

    def test_factory_accepts_overrides(self):
        """
        Caller-supplied keyword arguments override the factory defaults.
        A homeowner with an industrial 2.0 kW unit can supply that value
        and the factory must respect it instead of using the 1.5 kW default.
        """
        ac = ApplianceFactory.create(Appliance.AC, name='Industrial AC', power_rating_kw=2.0)

        assert ac.power_rating_kw == 2.0  # Override wins, not the 1.5 default
