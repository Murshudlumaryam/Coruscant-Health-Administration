from django import forms

from accounts.models import User
from documents.models import EncryptedDocument


class DocumentUploadForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset=User.objects.none(), required=False)

    class Meta:
        model = EncryptedDocument
        fields = ["title", "doc_type", "description", "owner", "file"]

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user.role in {"doctor", "administrator"} or user.is_superuser:
            self.fields["owner"].queryset = User.objects.filter(
                role="patient",
                is_approved=True,
            )
        else:
            self.fields["owner"].widget = forms.HiddenInput()

    def resolve_owner(self, request_user):
        return self.cleaned_data.get("owner") or request_user
