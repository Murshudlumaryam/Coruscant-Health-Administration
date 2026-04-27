from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.department_orders, name='department_orders'),
    path('orders/<int:order_id>/update/', views.update_order, name='update_order'),
]
