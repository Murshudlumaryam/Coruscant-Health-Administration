from django.contrib import admin
from .models import EmergencyPatient

@admin.register(EmergencyPatient)
class EmergencyPatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'severity', 'registered_at', 'is_resolved')
    list_filter = ('severity', 'is_resolved')
