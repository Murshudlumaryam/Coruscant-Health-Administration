from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MedicalOrderForm, MedicalReportForm
from .models import MedicalReport, MedicalOrder
from patients.models import HealthRecord
from accounts.models import User

@login_required
def write_report(request):
    if request.user.role != 'doctor' and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    
    form = MedicalReportForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            report = form.save(commit=False)
            report.doctor = request.user
            report.patient = form.cleaned_data['patient']
            report.is_visible_to_patient = form.cleaned_data['visible']
            report.save()
            messages.success(request, 'Report written successfully!')
            return redirect('doctor_reports')
        messages.error(request, next(iter(form.errors.values()))[0])

    return render(request, 'doctors/write_report.html', {'form': form})

@login_required
def doctor_reports(request):
    if request.user.role == 'doctor':
        reports = MedicalReport.objects.filter(doctor=request.user)
    else:
        reports = MedicalReport.objects.all()
    return render(request, 'doctors/reports.html', {'reports': reports})

@login_required
def create_order(request):
    if request.user.role != 'doctor' and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    
    form = MedicalOrderForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            order = form.save(commit=False)
            order.doctor = request.user
            order.patient = form.cleaned_data['patient']
            order.department = form.cleaned_data['department']
            order.save()
            messages.success(request, 'Medical order created!')
            return redirect('doctor_orders')
        messages.error(request, next(iter(form.errors.values()))[0])

    return render(request, 'doctors/create_order.html', {'form': form})

@login_required
def doctor_orders(request):
    if request.user.role == 'doctor':
        orders = MedicalOrder.objects.filter(doctor=request.user)
    else:
        orders = MedicalOrder.objects.all()
    return render(request, 'doctors/orders.html', {'orders': orders})

@login_required
def view_patient_detail(request, patient_id):
    if request.user.role not in ('doctor', 'administrator') and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    patient = get_object_or_404(User, id=patient_id, role='patient')
    records = HealthRecord.objects.filter(patient=patient)[:30]
    reports = MedicalReport.objects.filter(patient=patient)
    orders = MedicalOrder.objects.filter(patient=patient)
    return render(request, 'doctors/patient_detail.html', {
        'patient': patient, 'records': records, 'reports': reports, 'orders': orders
    })
