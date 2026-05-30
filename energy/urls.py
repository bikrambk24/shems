from django.urls import path

from energy import views

urlpatterns = [
    path('homeowner/dashboard/', views.dashboard, name='homeowner_dashboard'),
    path('homeowner/notifications/', views.notifications_list, name='notifications_list'),
    path('homeowner/notifications/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
]
