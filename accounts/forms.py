from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import HomeownerSettings, User


class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True, help_text='Required.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        """Force role=HOMEOWNER regardless of any POST manipulation."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # Hardcode role so public registration can never produce an admin/technician
        user.role = User.HOMEOWNER
        if commit:
            user.save()
        return user


class HomeownerSettingsForm(forms.ModelForm):

    class Meta:
        model = HomeownerSettings
        fields = ['daily_threshold_kwh']
        labels = {
            'daily_threshold_kwh': 'Daily usage alert threshold (kWh)',
        
        }
        help_texts = {
            'daily_threshold_kwh': 'You will receive an alert when your household '
                                   'exceeds this total on any single day.',
        }
