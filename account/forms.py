from django.forms import FileInput
from django import forms

from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    avatar = forms.ImageField(widget=FileInput, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'avatar')
