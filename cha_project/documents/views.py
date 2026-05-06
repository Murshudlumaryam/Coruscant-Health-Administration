from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .forms import DocumentUploadForm
from .models import EncryptedDocument
from .utils import encrypt_file, decrypt_file, compute_checksum

@login_required
def upload_document(request):
    form = DocumentUploadForm(request.user, request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            file = form.cleaned_data['file']
            raw = file.read()
            encrypted = encrypt_file(raw)
            checksum = compute_checksum(raw)
            owner = form.resolve_owner(request.user)

            doc = EncryptedDocument(
                owner=owner,
                uploaded_by=request.user,
                doc_type=form.cleaned_data['doc_type'],
                title=form.cleaned_data['title'] or file.name,
                original_filename=file.name,
                file_size=len(raw),
                is_encrypted=True,
                checksum=checksum,
                description=form.cleaned_data['description'],
            )
            from django.core.files.base import ContentFile

            doc.file.save(f"enc_{file.name}", ContentFile(encrypted))
            doc.save()

            messages.success(request, 'Document uploaded and encrypted securely!')
            return redirect('my_documents')
        messages.error(request, next(iter(form.errors.values()))[0])

    return render(request, 'documents/upload.html', {'form': form})

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
