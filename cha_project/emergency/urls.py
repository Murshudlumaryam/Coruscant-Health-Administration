from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_emergency, name='register_emergency'),
    path('list/', views.emergency_list, name='emergency_list'),
]
