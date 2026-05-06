from django import forms

from emergency.models import EmergencyPatient


class EmergencyRegistrationForm(forms.ModelForm):
    heart_rate = forms.CharField(required=False)
    blood_pressure = forms.CharField(required=False)
    temperature = forms.CharField(required=False)

    class Meta:
        model = EmergencyPatient
        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "chief_complaint",
            "severity",
            "notes",
        ]

    def build_initial_vitals(self):
        return {
            "heart_rate": self.cleaned_data.get("heart_rate", ""),
            "blood_pressure": self.cleaned_data.get("blood_pressure", ""),
            "temperature": self.cleaned_data.get("temperature", ""),
        }
