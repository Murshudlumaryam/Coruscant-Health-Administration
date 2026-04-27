from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MedicalReport, MedicalOrder, DoctorProfile
from patients.models import HealthRecord
from accounts.models import User
from departments.models import Department

@login_required
def write_report(request):
    if request.user.role != 'doctor' and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        patient = get_object_or_404(User, id=patient_id, role='patient')
        MedicalReport.objects.create(
            doctor=request.user,
            patient=patient,
            title=request.POST.get('title'),
            diagnosis=request.POST.get('diagnosis'),
            prescription=request.POST.get('prescription', ''),
            notes=request.POST.get('notes', ''),
            is_visible_to_patient=request.POST.get('visible', 'on') == 'on',
        )
        messages.success(request, 'Report written successfully!')
        return redirect('doctor_reports')
    
    patients = User.objects.filter(role='patient', is_approved=True)
    return render(request, 'doctors/write_report.html', {'patients': patients})

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
    
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        patient = get_object_or_404(User, id=patient_id, role='patient')
        dept_id = request.POST.get('department_id')
        dept = Department.objects.filter(id=dept_id).first() if dept_id else None
        MedicalOrder.objects.create(
            doctor=request.user,
            patient=patient,
            order_type=request.POST.get('order_type'),
            description=request.POST.get('description'),
            priority=request.POST.get('priority', 'normal'),
            department=dept,
        )
        messages.success(request, 'Medical order created!')
        return redirect('doctor_orders')
    
    patients = User.objects.filter(role='patient', is_approved=True)
    departments = Department.objects.filter(is_active=True)
    order_types = MedicalOrder.ORDER_TYPES
    return render(request, 'doctors/create_order.html', {
        'patients': patients, 'departments': departments, 'order_types': order_types
    })

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
