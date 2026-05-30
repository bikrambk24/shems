import pytest
from django.utils import timezone

from accounts.models import HomeownerSettings
from appliances.models import Appliance
from django.contrib.auth import get_user_model
from energy.models import EnergyUsage, Notification, NotificationLog


@pytest.mark.django_db
class TestObserverPattern:

    def test_threshold_breach_creates_notification_and_log(self, appliance, homeowner):
        # homeowner threshold = 10.0 kWh (set in conftest)
        # a single reading of 11.0 kWh pushes the daily total over the limit
        EnergyUsage.objects.create(
            appliance=appliance,
            kwh_consumed=11.0,
            recorded_at=timezone.now(),
        )
        # DashboardNotifier must have created a Notification for the homeowner
        assert Notification.objects.filter(user=homeowner).exists()
        # UsageLogger must have written an audit log entry
        assert NotificationLog.objects.filter(appliance=appliance, event_type='threshold_exceeded').exists()

    def test_no_notification_when_under_threshold(self, db):
        User = get_user_model()
        user = User.objects.create_user(username='charlie', password='test', role=User.HOMEOWNER)
        HomeownerSettings.objects.create(user=user, daily_threshold_kwh=10.0)
        appliance = Appliance.objects.create(
            name='Test Fridge', appliance_type=Appliance.FRIDGE,
            power_rating_kw=0.1, owner=user,
        )
        # 0.5 kWh is well under the 10.0 kWh threshold — no observers should fire
        EnergyUsage.objects.create(
            appliance=appliance,
            kwh_consumed=0.5,
            recorded_at=timezone.now(),
        )
        assert not Notification.objects.filter(user=user).exists()
        assert not NotificationLog.objects.filter(appliance=appliance).exists()

    def test_detaching_observer_stops_it_firing(self, db):
        from energy.observers import DashboardNotifier
        from core.ems import EnergyManagementSystem

        ems = EnergyManagementSystem()
        dashboard_notifier = next(
            (o for o in ems._observers if isinstance(o, DashboardNotifier)), None
        )
        assert dashboard_notifier is not None, "DashboardNotifier must be attached at startup"
        ems.detach(dashboard_notifier)

        try:
            User = get_user_model()
            user = User.objects.create_user(username='dave', password='test', role=User.HOMEOWNER)
            HomeownerSettings.objects.create(user=user, daily_threshold_kwh=0.1)
            appliance = Appliance.objects.create(
                name='Test Light', appliance_type=Appliance.LIGHT,
                power_rating_kw=0.06, owner=user,
            )
            # 1.0 kWh > 0.1 threshold — breach fires, but DashboardNotifier is detached
            EnergyUsage.objects.create(
                appliance=appliance,
                kwh_consumed=1.0,
                recorded_at=timezone.now(),
            )
            assert not Notification.objects.filter(user=user).exists()      # DashboardNotifier detached
            assert NotificationLog.objects.filter(appliance=appliance).exists()  # UsageLogger still fires

        finally:
            ems.attach(dashboard_notifier)  # restore so other tests are not affected
