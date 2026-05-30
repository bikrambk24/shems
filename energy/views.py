import json
from datetime import timedelta

from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from appliances.models import Appliance
from core.decorators import homeowner_required
from energy.models import EnergyUsage, Notification


def _calculate_bill(homeowner, start_date, end_date):
    try:
        plan = homeowner.homeownersettings.pricing_plan
        if not plan:
            return 0.0
    except Exception:
        return 0.0

    strategy = plan.get_strategy()  # Strategy pattern — picks the right billing algorithm

    usage_records = EnergyUsage.objects.filter(
        appliance__owner=homeowner,
        recorded_at__date__gte=start_date,
        recorded_at__date__lte=end_date,
    )

    total_pence = sum(
        strategy.calculate(record.kwh_consumed, record.recorded_at)
        for record in usage_records
    )
    return round(total_pence / 100, 2)  # pence → pounds


@homeowner_required
def dashboard(request):
    homeowner = request.user
    appliances = Appliance.objects.filter(owner=homeowner)

    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)
    date_range = [start_date + timedelta(days=i) for i in range(7)]
    date_labels = [d.strftime('%d %b') for d in date_range]

    # Build one dataset per appliance for the stacked bar chart (reads from DB)
    datasets = []
    for appliance in appliances:
        daily_totals = []
        for day in date_range:
            total = (
                EnergyUsage.objects
                .filter(appliance=appliance, recorded_at__date=day)
                .aggregate(total=Sum('kwh_consumed'))['total']
            ) or 0.0
            daily_totals.append(round(total, 2))
        datasets.append({'label': appliance.name, 'data': daily_totals})

    chart_data = json.dumps({'labels': date_labels, 'datasets': datasets})
    bill_estimate = _calculate_bill(homeowner, start_date, end_date)

    unread_notifications = Notification.objects.filter(user=homeowner, is_read=False)[:5]

    return render(request, 'homeowner/dashboard.html', {
        'chart_data': chart_data,
        'bill_estimate': bill_estimate,
        'unread_notifications': unread_notifications,
        'appliances': appliances,
        'start_date': start_date,
        'end_date': end_date,
    })


@homeowner_required
def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'homeowner/notifications.html', {'notifications': notifications})


@homeowner_required
def mark_notification_read(request, pk):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
    return redirect('notifications_list')
