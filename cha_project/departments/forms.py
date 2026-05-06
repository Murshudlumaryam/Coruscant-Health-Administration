from django import forms

from doctors.models import MedicalOrder


class OrderUpdateForm(forms.Form):
    status = forms.ChoiceField(choices=MedicalOrder.STATUS_CHOICES)
    findings = forms.CharField(required=False, widget=forms.Textarea)
    notes = forms.CharField(required=False, widget=forms.Textarea)
    report_file = forms.FileField(required=False)
