from django.contrib import admin
from .models import DoctorProfile, MedicalReport, MedicalOrder

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'license_number', 'department')

@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'doctor', 'patient', 'created_at')

@admin.register(MedicalOrder)
class MedicalOrderAdmin(admin.ModelAdmin):
    list_display = ('order_type', 'patient', 'doctor', 'priority', 'status', 'created_at')
    list_filter = ('status', 'priority', 'order_type')
