from django.contrib import admin
from .models import EncryptedDocument

@admin.register(EncryptedDocument)
class EncryptedDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'doc_type', 'is_encrypted', 'uploaded_at')
    list_filter = ('doc_type', 'is_encrypted')
