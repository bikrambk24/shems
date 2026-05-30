from django import forms

from accounts.models import User
from energy.models import FaultTicket


class AddTechnicianForm(forms.Form):
    """
    Admin form for creating a new technician account.
    Only admins reach this form (enforced by @admin_required on the view).
    """

    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
        help_text='Minimum 8 characters.',
    )

    def clean_username(self):
        """Check the username is not already taken."""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('A user with that username already exists.')
        return username


class UpdateTicketForm(forms.ModelForm):
    """
    Technician form for updating a fault ticket's status and adding notes.
    resolved_by is set in the view (not a form field) to prevent tampering.
    """

    class Meta:
        model = FaultTicket
        fields = ['status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
