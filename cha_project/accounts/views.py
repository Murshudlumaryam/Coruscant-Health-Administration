from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import User
from patients.models import PatientProfile, HealthRecord
from doctors.models import DoctorProfile, MedicalReport, MedicalOrder
from departments.models import Department
from emergency.models import EmergencyPatient
from documents.models import EncryptedDocument

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.role in ('patient', 'doctor') and not user.is_approved:
                messages.warning(request, 'Your account is pending administrator approval.')
                return render(request, 'accounts/login.html')
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role', 'patient')
        phone = request.POST.get('phone', '')
        
        if role not in ('patient', 'doctor'):
            messages.error(request, 'Invalid role selected.')
            return render(request, 'accounts/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name,
            role=role, phone=phone, is_approved=False, is_active=True
        )
        if role == 'patient':
            PatientProfile.objects.create(user=user)
        elif role == 'doctor':
            DoctorProfile.objects.create(user=user)

        messages.success(request, 'Registration successful! Awaiting administrator approval.')
        return redirect('login')
    return render(request, 'accounts/register.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    user = request.user
    ctx = {'user': user}
    
    if user.role == 'patient' or (user.is_superuser and request.GET.get('view') == 'patient'):
        ctx['health_records'] = HealthRecord.objects.filter(patient=user)[:10]
        ctx['reports'] = MedicalReport.objects.filter(patient=user, is_visible_to_patient=True)[:5]
        ctx['orders'] = MedicalOrder.objects.filter(patient=user)[:5]
        ctx['documents'] = EncryptedDocument.objects.filter(owner=user)[:5]
        return render(request, 'dashboard/patient.html', ctx)
    
    elif user.role == 'doctor':
        ctx['my_patients'] = User.objects.filter(patient_profile__assigned_doctor=user, role='patient')
        ctx['recent_reports'] = MedicalReport.objects.filter(doctor=user)[:5]
        ctx['pending_orders'] = MedicalOrder.objects.filter(doctor=user, status='pending')[:5]
        return render(request, 'dashboard/doctor.html', ctx)
    
    elif user.role == 'administrator' or user.is_superuser:
        ctx['pending_users'] = User.objects.filter(is_approved=False, role__in=['patient','doctor'])
        ctx['total_patients'] = User.objects.filter(role='patient').count()
        ctx['total_doctors'] = User.objects.filter(role='doctor').count()
        ctx['total_records'] = HealthRecord.objects.count()
        ctx['recent_users'] = User.objects.order_by('-date_joined')[:10]
        return render(request, 'dashboard/admin.html', ctx)
    
    elif user.role == 'emergency':
        ctx['recent_emergency'] = EmergencyPatient.objects.filter(registered_by=user)[:10]
        return render(request, 'dashboard/emergency.html', ctx)
    
    elif user.role == 'department':
        ctx['pending_orders'] = MedicalOrder.objects.filter(status='pending')[:10]
        ctx['in_progress_orders'] = MedicalOrder.objects.filter(status='in_progress')[:10]
        return render(request, 'dashboard/department.html', ctx)
    
    return render(request, 'dashboard/base_dashboard.html', ctx)

@login_required
def approve_user(request, user_id):
    if not (request.user.role == 'administrator' or request.user.is_superuser):
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    user = get_object_or_404(User, id=user_id)
    user.is_approved = True
    user.save()
    messages.success(request, f'{user.get_full_name()} has been approved.')
    return redirect('dashboard')

@login_required
def reject_user(request, user_id):
    if not (request.user.role == 'administrator' or request.user.is_superuser):
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    user = get_object_or_404(User, id=user_id)
    user.is_approved = False
    user.is_active = False
    user.save()
    messages.success(request, f'{user.get_full_name()} has been rejected.')
    return redirect('dashboard')
