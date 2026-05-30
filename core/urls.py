from django.urls import path

from core import views

urlpatterns = [
    # ── Admin panel ──────────────────────────────────────────────────────────
    # Prefix is /admin-panel/ (not /admin/) to avoid clashing with Django's
    # built-in admin at /django-admin/
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/homeowners/', views.admin_homeowners, name='admin_homeowners'),
    path('admin-panel/homeowners/<int:user_id>/toggle/', views.admin_toggle_user, name='admin_toggle_user'),
    path('admin-panel/technicians/', views.admin_technicians, name='admin_technicians'),
    path('admin-panel/pricing-plans/', views.admin_pricing_plans, name='admin_pricing_plans'),
    path('admin-panel/pricing-plans/<int:plan_id>/edit/', views.admin_edit_pricing_plan, name='admin_edit_pricing_plan'),
    path('admin-panel/notification-log/', views.admin_notification_log, name='admin_notification_log'),

    # ── Technician portal ────────────────────────────────────────────────────
    path('technician/', views.technician_dashboard, name='technician_dashboard'),
    path('technician/tickets/<int:pk>/', views.technician_ticket_detail, name='technician_ticket_detail'),
]
