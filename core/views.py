from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from core.decorators import admin_required, technician_required
from core.forms import AddTechnicianForm, UpdateTicketForm
from energy.models import FaultTicket, Notification, NotificationLog
from appliances.models import Appliance
from pricing.forms import PricingPlanForm
from pricing.models import PricingPlan


# Admin views

@admin_required
def admin_dashboard(request):
    context = {
        'homeowner_count': User.objects.filter(role=User.HOMEOWNER).count(),
        'technician_count': User.objects.filter(role=User.TECHNICIAN).count(),
        'open_tickets': FaultTicket.objects.filter(status=FaultTicket.OPEN).count(),
        'log_entries': NotificationLog.objects.count(),
        'appliance_count': Appliance.objects.count(),
    }
    return render(request, 'admin_panel/dashboard.html', context)


@admin_required
def admin_homeowners(request):
    homeowner_list = User.objects.filter(role=User.HOMEOWNER).order_by('username')
    paginator = Paginator(homeowner_list, per_page=10)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'admin_panel/homeowners.html', {'page_obj': page})


@admin_required
def admin_toggle_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        user.is_active = not user.is_active
        user.save()
        state = 'activated' if user.is_active else 'deactivated'
        messages.success(request, f'{user.username} has been {state}.')
    return redirect('admin_homeowners')


@admin_required
def admin_technicians(request):
    if request.method == 'POST':
        form = AddTechnicianForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data.get('email', ''),
                password=form.cleaned_data['password'],
                role=User.TECHNICIAN,
            )
            messages.success(request, f"Technician '{form.cleaned_data['username']}' created.")
            return redirect('admin_technicians')
    else:
        form = AddTechnicianForm()

    technicians = User.objects.filter(role=User.TECHNICIAN).order_by('username')
    return render(request, 'admin_panel/technicians.html', {
        'technicians': technicians,
        'form': form,
    })


@admin_required
def admin_pricing_plans(request):
    if request.method == 'POST':
        form = PricingPlanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pricing plan created.')
            return redirect('admin_pricing_plans')
    else:
        form = PricingPlanForm()

    plans = PricingPlan.objects.all().order_by('name')
    return render(request, 'admin_panel/pricing_plans.html', {'plans': plans, 'form': form})


@admin_required
def admin_edit_pricing_plan(request, plan_id):
    plan = get_object_or_404(PricingPlan, pk=plan_id)

    if request.method == 'POST':
        form = PricingPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{plan.name}" updated.')
            return redirect('admin_pricing_plans')
    else:
        form = PricingPlanForm(instance=plan)

    return render(request, 'admin_panel/pricing_plans.html', {
        'plans': PricingPlan.objects.all().order_by('name'),
        'form': form,
        'editing': plan,
    })


@admin_required
def admin_notification_log(request):
    log_list = NotificationLog.objects.select_related('appliance').order_by('-created_at')
    paginator = Paginator(log_list, per_page=20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'admin_panel/notification_log.html', {'page_obj': page})


# Technician views

@technician_required
def technician_dashboard(request):
    # Show all open and in-progress tickets across every home
    tickets = (
        FaultTicket.objects
        .filter(status__in=[FaultTicket.OPEN, FaultTicket.IN_PROGRESS])
        .select_related('appliance', 'appliance__owner')
        .order_by('-reported_at')
    )
    return render(request, 'technician/dashboard.html', {'tickets': tickets})


@technician_required
def technician_ticket_detail(request, pk):
    ticket = get_object_or_404(FaultTicket, pk=pk)

    if request.method == 'POST':
        form = UpdateTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            updated_ticket = form.save(commit=False)
            if updated_ticket.status == FaultTicket.RESOLVED:
                updated_ticket.resolved_by = request.user
                updated_ticket.appliance.is_faulty = False  # clear flag so homeowner UI updates
                updated_ticket.appliance.save()
            updated_ticket.save()

            # Notify the homeowner that their ticket has been updated
            homeowner = ticket.appliance.owner
            Notification.objects.create(
                user=homeowner,
                message=f'Your fault ticket for {ticket.appliance.name} has been updated to: {updated_ticket.status}.',
                level=Notification.INFO,
            )

            messages.success(request, f'Ticket #{ticket.pk} updated to {updated_ticket.status}.')
            return redirect('technician_dashboard')
    else:
        form = UpdateTicketForm(instance=ticket)

    return render(request, 'technician/ticket_detail.html', {
        'ticket': ticket,
        'form': form,
    })
