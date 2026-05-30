"""
tests/test_views.py — Integration tests for role-based access control.

Four tests that prove the three @role_required decorators work end-to-end:
  - A homeowner is blocked from the admin panel
  - A technician is blocked from appliance controls (homeowner-only area)
  - Public registration always creates a HOMEOWNER, never an elevated role
  - After login, each role is routed to its own dashboard, not a shared one
"""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
class TestRoleBasedAccessControl:

    def test_homeowner_cannot_access_admin_panel(self, client, homeowner):
        """
        @admin_required on admin_dashboard must redirect a homeowner away.

        A homeowner is a legitimate logged-in user, so this test confirms
        the decorator checks role, not just authentication status.
        Expected: HTTP 302 (redirect), not 200.
        """
        client.force_login(homeowner)
        response = client.get(reverse('admin_dashboard'))

        assert response.status_code == 302

    def test_technician_cannot_control_appliances(self, client, technician, appliance):
        """
        Appliance controls (toggle, delete, etc.) are protected by
        @homeowner_required.  A technician has no business controlling
        a homeowner's devices.

        Expected: HTTP 302 redirect away from the toggle endpoint.
        """
        client.force_login(technician)
        response = client.post(reverse('toggle_appliance', kwargs={'pk': appliance.pk}))

        assert response.status_code == 302

    def test_registration_only_creates_homeowner_role(self, client):
        """
        The public /register/ form must always produce a HOMEOWNER account.

        Admin and Technician accounts are created only by an admin inside
        the admin panel.  A malicious user cannot tamper with the form to
        gain elevated privileges — the view hard-codes role=HOMEOWNER.
        """
        client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })

        user = User.objects.get(username='newuser')
        assert user.role == User.HOMEOWNER

    def test_login_redirects_each_role_to_correct_dashboard(
        self, client, homeowner, admin_user, technician
    ):
        """
        After login, Django sends users to LOGIN_REDIRECT_URL (/role-redirect/).
        The role_redirect view then forwards each role to its own dashboard.

        This test checks the role_redirect logic directly using force_login,
        confirming that each role lands on a different URL.
        """
        # Homeowner → homeowner dashboard
        client.force_login(homeowner)
        response = client.get(reverse('role_redirect'))
        assert response.status_code == 302
        assert reverse('homeowner_dashboard') in response['Location']

        # Admin → admin dashboard
        client.force_login(admin_user)
        response = client.get(reverse('role_redirect'))
        assert response.status_code == 302
        assert reverse('admin_dashboard') in response['Location']

        # Technician → technician dashboard
        client.force_login(technician)
        response = client.get(reverse('role_redirect'))
        assert response.status_code == 302
        assert reverse('technician_dashboard') in response['Location']
