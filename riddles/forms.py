# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Employer, JobSeeker

class EmployerRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=100, required=True)
    company_description = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'role', 'company_name', 'company_description']
        widgets = {'password1': forms.PasswordInput(), 'password2': forms.PasswordInput}

class JobSeekerRegistrationForm(UserCreationForm):
    birthdate = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}))


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'role', 'birthdate']
        widgets = {'password1': forms.PasswordInput(), 'password2': forms.PasswordInput}
