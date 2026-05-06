from django import forms

from patients.models import HealthRecord


class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = [
            "heart_rate",
            "temperature",
            "blood_pressure_systolic",
            "blood_pressure_diastolic",
            "oxygen_saturation",
            "glucose_level",
            "weight",
            "notes",
            "source",
        ]

    def clean(self):
        cleaned_data = super().clean()
        monitored_values = [
            cleaned_data.get("heart_rate"),
            cleaned_data.get("temperature"),
            cleaned_data.get("blood_pressure_systolic"),
            cleaned_data.get("blood_pressure_diastolic"),
            cleaned_data.get("oxygen_saturation"),
            cleaned_data.get("glucose_level"),
            cleaned_data.get("weight"),
        ]
        if not any(value is not None for value in monitored_values) and not cleaned_data.get(
            "notes"
        ):
            raise forms.ValidationError(
                "Provide at least one reading or add a note for this upload."
            )
        return cleaned_data
