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


    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('Username already exists')
        return data

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match')
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already exists')
        return data

class UserEditForm(forms.ModelForm):
    avatar = forms.ImageField(widget=FileInput, required=False)
    class Meta:
        model = User
        fields = ('username', 'email', 'avatar')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists() and data != self.user.username:
            raise forms.ValidationError('Username already exists')
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists() and data != self.user.email:
            raise forms.ValidationError('Email already exists')
        return data