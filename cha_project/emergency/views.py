from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EmergencyPatient

@login_required
def register_emergency(request):
    if request.user.role not in ('emergency', 'administrator', 'doctor') and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        EmergencyPatient.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            date_of_birth=request.POST.get('date_of_birth') or None,
            gender=request.POST.get('gender', 'O'),
            chief_complaint=request.POST.get('chief_complaint'),
            severity=request.POST.get('severity', 'moderate'),
            registered_by=request.user,
            initial_vitals={
                'heart_rate': request.POST.get('heart_rate', ''),
                'blood_pressure': request.POST.get('blood_pressure', ''),
                'temperature': request.POST.get('temperature', ''),
            },
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'Emergency patient registered!')
        return redirect('emergency_list')
    return render(request, "emergency/register.html", {"severity_choices": EP.SEVERITY})

@login_required
def emergency_list(request):
    patients = EmergencyPatient.objects.filter(is_resolved=False)
    return render(request, 'emergency/list.html', {'patients': patients})

from .models import EmergencyPatient as EP
