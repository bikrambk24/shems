from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from appliances.factories import ApplianceFactory
from appliances.forms import ApplianceAddForm, ApplianceEditForm
from appliances.models import Appliance
from core.decorators import homeowner_required
from core.ems import EnergyManagementSystem
from energy.models import EnergyUsage, FaultTicket


@homeowner_required
def list_appliances(request):
    """Show all appliances belonging to the logged-in homeowner, plus the add form."""
    appliances = Appliance.objects.filter(owner=request.user).order_by('name')
    add_form = ApplianceAddForm()
    return render(request, 'homeowner/appliances.html', {
        'appliances': appliances,
        'add_form': add_form,
    })


@homeowner_required
def add_appliance(request):
    """
    Create a new appliance via the Factory pattern.

    The factory supplies sensible defaults for the selected appliance type
    (e.g. 1.5 kW for an AC).  The homeowner can override the power rating
    by filling in the optional field.
    """
    if request.method == 'POST':
        form = ApplianceAddForm(request.POST)
        if form.is_valid():
            appliance_type = form.cleaned_data['appliance_type']
            name = form.cleaned_data['name']
            custom_power = form.cleaned_data.get('power_rating_kw')

            kwargs = {'name': name, 'owner': request.user}
            if custom_power:
                # Override the factory default with the user's custom value
                kwargs['power_rating_kw'] = custom_power

            # ★ FACTORY PATTERN: create() picks defaults based on appliance_type
            appliance = ApplianceFactory.create(appliance_type, **kwargs)
            appliance.save()

            # ★ SINGLETON: register with the central EMS after saving
            ems = EnergyManagementSystem()
            ems.register_appliance(appliance)

            messages.success(request, f'{appliance.name} added (default {appliance.power_rating_kw} kW).')
    else:
        messages.error(request, 'Invalid form submission.')

    return redirect('list_appliances')


@homeowner_required
def edit_appliance(request, pk):
    """Edit an existing appliance's name and power rating."""
    appliance = get_object_or_404(Appliance, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = ApplianceEditForm(request.POST, instance=appliance)
        if form.is_valid():
            form.save()
            messages.success(request, f'{appliance.name} updated.')
            return redirect('list_appliances')
    else:
        form = ApplianceEditForm(instance=appliance)

    appliances = Appliance.objects.filter(owner=request.user).order_by('name')
    return render(request, 'homeowner/appliances.html', {
        'appliances': appliances,
        'edit_form': form,
        'editing': appliance,
        'add_form': ApplianceAddForm(),
    })


@homeowner_required
def delete_appliance(request, pk):
    """Delete an appliance (POST only)."""
    if request.method == 'POST':
        appliance = get_object_or_404(Appliance, pk=pk, owner=request.user)
        name = appliance.name
        appliance.delete()
        messages.success(request, f'{name} deleted.')
    return redirect('list_appliances')


@homeowner_required
def toggle_appliance(request, pk):
    if request.method == 'POST':
        appliance = get_object_or_404(Appliance, pk=pk, owner=request.user)
        appliance.is_on = not appliance.is_on
        appliance.save()
        state = 'ON' if appliance.is_on else 'OFF'

        if not appliance.is_on:
            # Turning OFF, record one hour of usage at rated power
            # This creates an EnergyUsage row, which triggers the Observer chain
            # (threshold check -> dashboard notification -> audit log)
            EnergyUsage.objects.create(
                appliance=appliance,
                kwh_consumed=appliance.power_rating_kw,
                recorded_at=timezone.now(),
            )
            messages.success(request, f'{appliance.name} turned OFF — usage recorded.')
        else:
            messages.success(request, f'{appliance.name} turned ON.')
    return redirect('list_appliances')


@homeowner_required
def report_fault(request, pk):
    """
    Manually report a fault on an appliance (POST only).
    Creates a FaultTicket visible to technicians.
    """
    if request.method == 'POST':
        appliance = get_object_or_404(Appliance, pk=pk, owner=request.user)

        # Avoid duplicate open tickets for the same appliance
        already_open = FaultTicket.objects.filter(
            appliance=appliance,
            status__in=[FaultTicket.OPEN, FaultTicket.IN_PROGRESS],
        ).exists()

        if already_open:
            messages.warning(request, f'A fault ticket for {appliance.name} is already open.')
        else:
            appliance.is_faulty = True
            appliance.save()
            FaultTicket.objects.create(
                appliance=appliance,
                notes='Reported manually by homeowner.',
            )
            messages.success(request, f'Fault reported for {appliance.name}. A technician will investigate.')

    return redirect('list_appliances')
