from django.db import models
from accounts.models import User

class EmergencyPatient(models.Model):
    SEVERITY = [
        ('critical', 'Critical'),
        ('severe', 'Severe'),
        ('moderate', 'Moderate'),
        ('minor', 'Minor'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M','Male'),('F','Female'),('O','Other')], default='O')
    chief_complaint = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY, default='moderate')
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    linked_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='emergency_records')
    initial_vitals = models.JSONField(default=dict, blank=True)
    notes = models.TextField(blank=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-registered_at']

    def __str__(self):
        return f"Emergency: {self.first_name} {self.last_name} - {self.severity}"
