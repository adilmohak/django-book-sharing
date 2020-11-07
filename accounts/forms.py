from django import forms
from django.contrib.auth.forms import PasswordResetForm

from .models import User


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = "This is not the email you registered. Try another one!"
            self.add_error('email', msg)
            return email


class UserCreateForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'type': 'email', 'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'type': 'password', 'class': 'form-control'})

    class Meta:
        model = User
        fields = [
            'email', 'password'
        ]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email', 'name', 'location', 'image'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['location'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
