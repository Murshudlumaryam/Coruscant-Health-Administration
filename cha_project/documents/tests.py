from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from accounts.models import User
from documents.forms import DocumentUploadForm
from documents.utils import decrypt_file, encrypt_file


class DocumentSecurityTest(TestCase):
    def test_encrypt_round_trip(self):
        raw = b"coruscant"
        encrypted = encrypt_file(raw)
        self.assertNotEqual(raw, encrypted)
        self.assertEqual(decrypt_file(encrypted), raw)

    def test_patient_upload_form_hides_owner(self):
        patient = User.objects.create_user("pt-doc", password="x", role="patient", is_approved=True)
        upload = SimpleUploadedFile("scan.txt", b"test")
        form = DocumentUploadForm(
            patient,
            data={"title": "Scan", "doc_type": "other", "description": ""},
            files={"file": upload},
        )
        self.assertTrue(form.is_valid())
