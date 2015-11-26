from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm




class UsuarioEditarForm(ModelForm):
    class Meta:
        model = User
        exclude = ['password']
        fields = ['username', 'email', 'first_name', 'last_name']




class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput(),
        }

