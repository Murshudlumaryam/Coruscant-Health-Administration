from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import HealthRecord, PatientProfile
from accounts.models import User

@login_required
def upload_health_data(request):
    if request.method == 'POST':
        data = {
            'patient': request.user,
            'heart_rate': request.POST.get('heart_rate') or None,
            'temperature': request.POST.get('temperature') or None,
            'blood_pressure_systolic': request.POST.get('bp_systolic') or None,
            'blood_pressure_diastolic': request.POST.get('bp_diastolic') or None,
            'oxygen_saturation': request.POST.get('oxygen_saturation') or None,
            'glucose_level': request.POST.get('glucose_level') or None,
            'weight': request.POST.get('weight') or None,
            'notes': request.POST.get('notes', ''),
            'source': request.POST.get('source', 'manual'),
        }
        HealthRecord.objects.create(**data)
        messages.success(request, 'Health data uploaded successfully!')
        return redirect('patient_records')
    return render(request, 'patients/upload_health.html')

@login_required
def patient_records(request):
    if request.user.role == 'patient':
        records = HealthRecord.objects.filter(patient=request.user)
    else:
        patient_id = request.GET.get('patient_id')
        if patient_id:
            records = HealthRecord.objects.filter(patient_id=patient_id)
        else:
            records = HealthRecord.objects.none()
    
    records_data = list(records.values('recorded_at', 'heart_rate', 'temperature',
        'blood_pressure_systolic', 'blood_pressure_diastolic', 'oxygen_saturation',
        'glucose_level', 'weight', 'notes', 'source'))
    
    return render(request, 'patients/records.html', {
        'records': records[:50],
        'records_data': records_data,
    })

@login_required
def all_patients(request):
    if request.user.role not in ('doctor', 'administrator') and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    
    patients = User.objects.filter(role='patient', is_approved=True)
    return render(request, 'patients/list.html', {'patients': patients})
