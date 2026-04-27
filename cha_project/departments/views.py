from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Department, OrderResult
from doctors.models import MedicalOrder

@login_required
def department_orders(request):
    orders = MedicalOrder.objects.filter(status__in=['pending', 'in_progress'])
    return render(request, 'departments/orders.html', {'orders': orders})

@login_required
def update_order(request, order_id):
    order = get_object_or_404(MedicalOrder, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        
        findings = request.POST.get('findings', '')
        if findings:
            result, created = OrderResult.objects.get_or_create(order=order, defaults={'uploaded_by': request.user, 'findings': findings})
            if not created:
                result.findings = findings
                result.notes = request.POST.get('notes', '')
                if request.FILES.get('report_file'):
                    result.report_file = request.FILES['report_file']
                result.save()
        
        messages.success(request, 'Order updated!')
        return redirect('department_orders')
    return render(request, 'departments/update_order.html', {'order': order, 'status_choices': MedicalOrder.STATUS_CHOICES})
