from django.db import models
from accounts.models import User

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialty = models.CharField(max_length=100, blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)
    years_of_experience = models.IntegerField(default=0)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

class MedicalReport(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_written')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_reports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    diagnosis = models.TextField()
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    is_visible_to_patient = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Report: {self.title} for {self.patient.username}"

class MedicalOrder(models.Model):
    ORDER_TYPES = [
        ('ct_scan', 'CT Scan'),
        ('pet_scan', 'PET Scan'),
        ('mri', 'MRI'),
        ('xray', 'X-Ray'),
        ('blood_test', 'Blood Test'),
        ('urine_test', 'Urine Test'),
        ('ecg', 'ECG'),
        ('ultrasound', 'Ultrasound'),
        ('biopsy', 'Biopsy'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_created')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_type = models.CharField(max_length=30, choices=ORDER_TYPES)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=[('low','Low'),('normal','Normal'),('high','High'),('urgent','Urgent')], default='normal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_order_type_display()} for {self.patient.username}"
