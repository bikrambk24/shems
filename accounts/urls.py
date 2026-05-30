from django.contrib.auth import views as auth_views
from django.urls import path

from accounts import views

urlpatterns = [
    # Django's built-in LoginView — we just point it at our custom template
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            redirect_authenticated_user=True,  # already-logged-in users go to LOGIN_REDIRECT_URL
        ),
        name='login',
    ),
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('register/', views.register, name='register'),
    path('role-redirect/', views.role_redirect, name='role_redirect'),
    path('homeowner/settings/', views.homeowner_settings, name='homeowner_settings'),
]
