"""
tests/test_singleton.py — Tests for the Singleton Pattern (core/ems.py)

Two tests that prove the single most important guarantee of the Singleton:
no matter how many times we call EnergyManagementSystem(), we always get
back the exact same object — one shared instance, never a copy.
"""

from core.ems import EnergyManagementSystem
from core.patterns import Observer


class _DummyObserver(Observer):
    """Minimal observer used only by these tests — does nothing on update."""
    def update(self, event_data):
        pass


class TestSingletonPattern:

    def test_two_instances_are_same_object(self):
        """
        Core Singleton guarantee: EnergyManagementSystem() called twice must
        return the exact same Python object, not two equal-looking copies.

        Python's 'is' operator checks identity (same memory address).
        Two separate objects could pass == but would never pass 'is'.
        """
        ems1 = EnergyManagementSystem()
        ems2 = EnergyManagementSystem()

        assert ems1 is ems2

    def test_state_persists_across_instance_fetches(self):
        """
        Because both variables point to one shared object, any change made
        through one reference is immediately visible through the other.

        We attach a dummy observer via ems1, then fetch ems2 independently
        and confirm the observer is already there — proving it is truly one
        shared object, not two objects that happen to look alike.
        """
        ems1 = EnergyManagementSystem()
        dummy = _DummyObserver()
        ems1.attach(dummy)

        ems2 = EnergyManagementSystem()
        assert dummy in ems2._observers

        ems1.detach(dummy)  # Clean up so this test does not affect others
