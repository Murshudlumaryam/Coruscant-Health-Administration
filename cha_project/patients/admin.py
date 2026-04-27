from django.contrib import admin
from .models import PatientProfile, HealthRecord

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_type', 'assigned_doctor')

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'recorded_at', 'heart_rate', 'temperature', 'source')
    list_filter = ('source',)
