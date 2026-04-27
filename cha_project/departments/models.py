from django.db import models
from accounts.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_departments')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class OrderResult(models.Model):
    order = models.OneToOneField('doctors.MedicalOrder', on_delete=models.CASCADE, related_name='result')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    findings = models.TextField()
    report_file = models.FileField(upload_to='order_results/', blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Result for {self.order}"
