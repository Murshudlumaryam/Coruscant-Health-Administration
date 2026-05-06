from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderUpdateForm
from .models import OrderResult
from doctors.models import MedicalOrder

@login_required
def department_orders(request):
    orders = MedicalOrder.objects.filter(status__in=['pending', 'in_progress'])
    return render(request, 'departments/orders.html', {'orders': orders})

@login_required
def update_order(request, order_id):
    order = get_object_or_404(MedicalOrder, id=order_id)
    form = OrderUpdateForm(request.POST or None, request.FILES or None, initial={'status': order.status})
    if request.method == 'POST':
        if form.is_valid():
            order.status = form.cleaned_data['status']
            order.save(update_fields=['status'])

            findings = form.cleaned_data['findings']
            if findings:
                result, created = OrderResult.objects.get_or_create(
                    order=order,
                    defaults={
                        'uploaded_by': request.user,
                        'findings': findings,
                        'notes': form.cleaned_data['notes'],
                        'report_file': form.cleaned_data['report_file'],
                    },
                )
                if not created:
                    result.findings = findings
                    result.notes = form.cleaned_data['notes']
                    if form.cleaned_data['report_file']:
                        result.report_file = form.cleaned_data['report_file']
                    result.save()

            messages.success(request, 'Order updated!')
            return redirect('department_orders')
        messages.error(request, next(iter(form.errors.values()))[0])
    return render(request, 'departments/update_order.html', {'order': order, 'form': form})
