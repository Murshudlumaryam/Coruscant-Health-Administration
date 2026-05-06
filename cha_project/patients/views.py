from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import HealthRecordForm
from .models import HealthRecord
from accounts.models import User

@login_required
def upload_health_data(request):
    form = HealthRecordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = request.user
            record.save()
            messages.success(request, 'Health data uploaded successfully!')
            return redirect('patient_records')
        messages.error(request, next(iter(form.errors.values()))[0])
    return render(request, 'patients/upload_health.html', {'form': form})

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
