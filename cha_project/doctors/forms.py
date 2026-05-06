from django import forms

from accounts.models import User
from departments.models import Department
from doctors.models import MedicalOrder, MedicalReport


class MedicalReportForm(forms.ModelForm):
    patient = forms.ModelChoiceField(queryset=User.objects.none())
    visible = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = MedicalReport
        fields = ["patient", "title", "diagnosis", "prescription", "notes", "visible"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["patient"].queryset = User.objects.filter(
            role="patient",
            is_approved=True,
        )


class MedicalOrderForm(forms.ModelForm):
    patient = forms.ModelChoiceField(queryset=User.objects.none())
    department = forms.ModelChoiceField(
        queryset=Department.objects.none(),
        required=False,
    )

    class Meta:
        model = MedicalOrder
        fields = ["patient", "order_type", "description", "priority", "department"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["patient"].queryset = User.objects.filter(
            role="patient",
            is_approved=True,
        )
        self.fields["department"].queryset = Department.objects.filter(is_active=True)
