from django import forms
from django.contrib.auth import authenticate

from accounts.models import User
from doctors.models import DoctorProfile
from patients.models import PatientProfile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            self.user = authenticate(
                self.request,
                username=username,
                password=password,
            )
            if self.user is None:
                raise forms.ValidationError("Invalid username or password.")
        return cleaned_data

    def get_user(self):
        return self.user


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "password",
            "role",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].choices = [
            ("patient", "Patient"),
            ("doctor", "Doctor"),
        ]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")
        return username

    def clean_role(self):
        role = self.cleaned_data["role"]
        if role not in {"patient", "doctor"}:
            raise forms.ValidationError("Invalid role selected.")
        return role

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            role=self.cleaned_data["role"],
            phone=self.cleaned_data.get("phone", ""),
            is_approved=False,
            is_active=True,
        )
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            if user.role == "patient":
                PatientProfile.objects.get_or_create(user=user)
            if user.role == "doctor":
                DoctorProfile.objects.get_or_create(user=user)
        return user
