from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import EncryptedDocument
from .utils import encrypt_file, decrypt_file, compute_checksum
from accounts.models import User

@login_required
def upload_document(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            messages.error(request, 'No file selected.')
            return redirect('upload_document')
        
        raw = file.read()
        encrypted = encrypt_file(raw)
        checksum = compute_checksum(raw)
        
        owner_id = request.POST.get('owner_id')
        if owner_id and (request.user.role in ('doctor', 'administrator') or request.user.is_superuser):
            owner = get_object_or_404(User, id=owner_id)
        else:
            owner = request.user
        
        doc = EncryptedDocument(
            owner=owner,
            uploaded_by=request.user,
            doc_type=request.POST.get('doc_type', 'other'),
            title=request.POST.get('title', file.name),
            original_filename=file.name,
            file_size=len(raw),
            is_encrypted=True,
            checksum=checksum,
            description=request.POST.get('description', ''),
        )
        from django.core.files.base import ContentFile
        doc.file.save(f"enc_{file.name}", ContentFile(encrypted))
        doc.save()
        
        messages.success(request, 'Document uploaded and encrypted securely!')
        return redirect('my_documents')
    
    patients = User.objects.filter(role='patient', is_approved=True) if request.user.role in ('doctor', 'administrator') else []
    return render(request, 'documents/upload.html', {
        'patients': patients,
        'doc_types': EncryptedDocument.DOC_TYPES,
    })

@login_required
def my_documents(request):
    if request.user.role in ('administrator',) or request.user.is_superuser:
        docs = EncryptedDocument.objects.all()
    else:
        docs = EncryptedDocument.objects.filter(owner=request.user)
    return render(request, 'documents/list.html', {'documents': docs})

@login_required
def download_document(request, doc_id):
    doc = get_object_or_404(EncryptedDocument, id=doc_id)
    if doc.owner != request.user and request.user.role not in ('doctor', 'administrator') and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('my_documents')
    
    encrypted_data = doc.file.read()
    decrypted = decrypt_file(encrypted_data)
    
    response = HttpResponse(decrypted, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{doc.original_filename}"'
    return response
