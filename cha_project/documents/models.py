from django.db import models
from accounts.models import User
import os

class EncryptedDocument(models.Model):
    DOC_TYPES = [
        ('lab_result', 'Lab Result'),
        ('prescription', 'Prescription'),
        ('imaging', 'Imaging'),
        ('insurance', 'Insurance'),
        ('id_document', 'ID Document'),
        ('consent_form', 'Consent Form'),
        ('other', 'Other'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents_uploaded')
    doc_type = models.CharField(max_length=30, choices=DOC_TYPES, default='other')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='encrypted_docs/')
    original_filename = models.CharField(max_length=255)
    file_size = models.IntegerField(default=0)
    is_encrypted = models.BooleanField(default=True)
    checksum = models.CharField(max_length=64, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} ({self.owner.username})"
