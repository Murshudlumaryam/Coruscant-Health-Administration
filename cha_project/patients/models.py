from django.db import models
from accounts.models import User

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    blood_type = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    insurance_number = models.CharField(max_length=50, blank=True)
    assigned_doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='patients')

    def __str__(self):
        return f"Profile: {self.user.get_full_name()}"

class HealthRecord(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_records')
    recorded_at = models.DateTimeField(auto_now_add=True)
    heart_rate = models.FloatField(null=True, blank=True, help_text="bpm")
    temperature = models.FloatField(null=True, blank=True, help_text="°C")
    blood_pressure_systolic = models.IntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True)
    oxygen_saturation = models.FloatField(null=True, blank=True, help_text="%")
    glucose_level = models.FloatField(null=True, blank=True, help_text="mg/dL")
    weight = models.FloatField(null=True, blank=True, help_text="kg")
    notes = models.TextField(blank=True)
    source = models.CharField(max_length=50, default='manual', choices=[
        ('manual', 'Manual Entry'), ('device', 'Device Upload'), ('emergency', 'Emergency')
    ])

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.patient.username} - {self.recorded_at.strftime('%Y-%m-%d %H:%M')}"
