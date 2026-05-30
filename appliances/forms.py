from django import forms

from appliances.models import Appliance


class ApplianceAddForm(forms.Form):

    name = forms.CharField(
        max_length=100,
        label='Appliance name',
        help_text='e.g. "Kitchen Fridge" or "Living Room AC"',
    )
    appliance_type = forms.ChoiceField(
        choices=Appliance.TYPE_CHOICES,
        label='Type',
    )
    power_rating_kw = forms.FloatField(
        required=False,
        min_value=0.001,
        label='Custom power rating (kW)',
        help_text='',
    )


class ApplianceEditForm(forms.ModelForm):

    class Meta:
        model = Appliance
        fields = ['name', 'power_rating_kw']
        labels = {'power_rating_kw': 'Power rating (kW)'}
