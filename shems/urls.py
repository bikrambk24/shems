"""
Root URL configuration for SHEMS.

URL layout:
  /                    → redirects to login
  /login/              → Django's built-in LoginView (accounts app)
  /logout/             → logout form POST (accounts app)
  /register/           → homeowner self-registration (accounts app)
  /role-redirect/      → post-login role router (accounts app)

  /homeowner/...       → homeowner views (energy + appliances + pricing apps)
  /admin-panel/...     → custom admin views (core app)
                         NOTE: named 'admin-panel' not 'admin' to avoid
                         clashing with Django's built-in /django-admin/
  /technician/...      → technician views (core app)

  /django-admin/       → Django's built-in admin (for superuser access)
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Django's built-in admin — kept at /django-admin/ to avoid name clash
    path('django-admin/', admin.site.urls),

    # Redirect bare root to login
    path('', RedirectView.as_view(url='/login/', permanent=False)),

    # Auth + registration routes
    path('', include('accounts.urls')),

    # Homeowner feature routes (appliances, energy/dashboard, pricing)
    path('', include('appliances.urls')),
    path('', include('energy.urls')),
    path('', include('pricing.urls')),

    # Admin panel + technician routes
    path('', include('core.urls')),
]
