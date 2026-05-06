from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EmergencyRegistrationForm
from .models import EmergencyPatient

@login_required
def register_emergency(request):
    if request.user.role not in ('emergency', 'administrator', 'doctor') and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    
    form = EmergencyRegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            emergency_case = form.save(commit=False)
            emergency_case.registered_by = request.user
            emergency_case.initial_vitals = form.build_initial_vitals()
            emergency_case.save()
            messages.success(request, 'Emergency patient registered!')
            return redirect('emergency_list')
        messages.error(request, next(iter(form.errors.values()))[0])
    return render(request, "emergency/register.html", {"form": form, "severity_choices": EP.SEVERITY})

@login_required
def emergency_list(request):
    patients = EmergencyPatient.objects.filter(is_resolved=False)
    return render(request, 'emergency/list.html', {'patients': patients})

from .models import EmergencyPatient as EP
