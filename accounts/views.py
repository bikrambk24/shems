from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.forms import HomeownerSettingsForm, RegisterForm
from accounts.models import HomeownerSettings
from core.decorators import homeowner_required


def register(request):
    if request.user.is_authenticated:
        return redirect('role_redirect')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            HomeownerSettings.objects.create(user=user)  # create settings record with defaults
            login(request, user)  # log in immediately so they land on their dashboard
            messages.success(request, f'Welcome, {user.username}! Your account is ready.')
            return redirect('homeowner_dashboard')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def role_redirect(request):
    # Routes each role to its own dashboard after login (LOGIN_REDIRECT_URL points here)
    user = request.user
    if user.is_homeowner():
        return redirect('homeowner_dashboard')
    elif user.is_admin_user():
        return redirect('admin_dashboard')
    elif user.is_technician():
        return redirect('technician_dashboard')
    return redirect('login')


@homeowner_required
def homeowner_settings(request):
    settings_obj = request.user.homeownersettings

    if request.method == 'POST':
        form = HomeownerSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully.')
            return redirect('homeowner_settings')
    else:
        form = HomeownerSettingsForm(instance=settings_obj)

    return render(request, 'homeowner/settings.html', {'form': form})
