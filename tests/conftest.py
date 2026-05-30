import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


# Shared fixtures — automatically available in all test files without importing

@pytest.fixture
def homeowner(db):
    from accounts.models import HomeownerSettings
    user = User.objects.create_user(username='alice', password='testpass123', role=User.HOMEOWNER)
    HomeownerSettings.objects.create(user=user, daily_threshold_kwh=10.0)
    return user


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(username='sysadmin', password='testpass123', role=User.ADMIN)


@pytest.fixture
def technician(db):
    return User.objects.create_user(username='tech1', password='testpass123', role=User.TECHNICIAN)


@pytest.fixture
def appliance(homeowner):
    from appliances.models import Appliance
    return Appliance.objects.create(
        name='Living Room AC',
        appliance_type=Appliance.AC,
        power_rating_kw=1.5,
        owner=homeowner,
    )
