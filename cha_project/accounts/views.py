from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from accounts.forms import LoginForm, RegistrationForm
from .models import User
from .services import build_dashboard, set_approval_state

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            if user.role in ('patient', 'doctor') and not user.is_approved:
                messages.warning(request, 'Your account is pending administrator approval.')
                return render(request, 'accounts/login.html', {'form': form})
            login(request, user)
            return redirect('dashboard')
        messages.error(request, form.errors.get('__all__', ['Invalid username or password.'])[0])
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Awaiting administrator approval.')
            return redirect('login')
        messages.error(request, next(iter(form.errors.values()))[0])
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    template_name, context = build_dashboard(request.user)
    context['user'] = request.user
    return render(request, template_name, context)

@login_required
def approve_user(request, user_id):
    if not (request.user.role == 'administrator' or request.user.is_superuser):
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    user = get_object_or_404(User, id=user_id)
    set_approval_state(user, approved=True)
    messages.success(request, f'{user.get_full_name()} has been approved.')
    return redirect('dashboard')

@login_required
def reject_user(request, user_id):
    if not (request.user.role == 'administrator' or request.user.is_superuser):
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    user = get_object_or_404(User, id=user_id)
    set_approval_state(user, approved=False)
    messages.success(request, f'{user.get_full_name()} has been rejected.')
    return redirect('dashboard')


def health_check(request):
    return HttpResponse('ok', content_type='text/plain')
