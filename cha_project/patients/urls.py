from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_health_data, name='upload_health'),
    path('records/', views.patient_records, name='patient_records'),
    path('list/', views.all_patients, name='all_patients'),
]
