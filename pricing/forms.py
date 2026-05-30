from django import forms

from pricing.models import PricingPlan


class SwitchPlanForm(forms.Form):
    """
    Simple form for a homeowner to switch their active pricing plan.
    Only active plans appear in the dropdown.
    """

    pricing_plan = forms.ModelChoiceField(
        queryset=PricingPlan.objects.filter(is_active=True),
        label='Select a pricing plan',
        empty_label='-- Choose a plan --',
    )


class PricingPlanForm(forms.ModelForm):
    """Admin form for creating or editing a pricing plan."""

    class Meta:
        model = PricingPlan
        fields = [
            'name', 'strategy_type',
            'base_rate', 'peak_rate', 'peak_start_hour', 'peak_end_hour',
            'green_discount_percent', 'is_active',
        ]
        help_texts = {
            'base_rate': 'Cost per kWh in pence (e.g. 28.0)',
            'peak_rate': 'Used by Time of Use plans only.',
            'peak_start_hour': '0–23 (e.g. 7 = 7 am). Time of Use only.',
            'peak_end_hour': '0–23 (e.g. 22 = 10 pm). Time of Use only.',
            'green_discount_percent': 'e.g. 10 = 10% off. Green Energy only.',
        }
