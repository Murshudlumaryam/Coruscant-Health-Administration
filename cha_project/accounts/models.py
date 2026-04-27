from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('administrator', 'Administrator'),
        ('emergency', 'Emergency Services'),
        ('department', 'Department'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    is_approved = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"

    @property
    def is_admin(self):
        return self.role == 'administrator' or self.is_superuser

    @property
    def needs_approval(self):
        return self.role in ('patient', 'doctor') and not self.is_approved
