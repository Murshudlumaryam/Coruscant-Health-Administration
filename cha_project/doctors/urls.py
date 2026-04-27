from django.urls import path
from . import views

urlpatterns = [
    path('report/write/', views.write_report, name='write_report'),
    path('reports/', views.doctor_reports, name='doctor_reports'),
    path('order/create/', views.create_order, name='create_order'),
    path('orders/', views.doctor_orders, name='doctor_orders'),
    path('patient/<int:patient_id>/', views.view_patient_detail, name='patient_detail'),
]
