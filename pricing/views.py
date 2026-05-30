from django.contrib import messages
from django.shortcuts import redirect, render

from core.decorators import homeowner_required
from pricing.forms import SwitchPlanForm
from pricing.models import PricingPlan


@homeowner_required
def pricing_plan_page(request):
    """
    Show the homeowner's current pricing plan and let them switch to another.

    On POST: updates HomeownerSettings.pricing_plan and redirects back.
    On GET:  shows the current plan details + a dropdown of all active plans.
    """
    homeowner_settings = request.user.homeownersettings
    current_plan = homeowner_settings.pricing_plan
    all_active_plans = PricingPlan.objects.filter(is_active=True)

    if request.method == 'POST':
        form = SwitchPlanForm(request.POST)
        if form.is_valid():
            new_plan = form.cleaned_data['pricing_plan']
            homeowner_settings.pricing_plan = new_plan
            homeowner_settings.save()
            messages.success(request, f'Switched to "{new_plan.name}" successfully.')
            return redirect('pricing_plan_page')
    else:
        form = SwitchPlanForm(initial={'pricing_plan': current_plan})

    return render(request, 'homeowner/pricing.html', {
        'current_plan': current_plan,
        'all_active_plans': all_active_plans,
        'form': form,
    })
