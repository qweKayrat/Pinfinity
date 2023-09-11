from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .models import User


# class RegisterUserForm(UserCreationForm):
#     username = forms.CharField(label='Логин',
#                                widget=forms.TextInput(attrs={'class': 'form-input'}))
#     email = forms.EmailField(label='Почта',
#                              widget=forms.EmailInput(attrs={'class': 'form-input'}))
#     password1 = forms.CharField(label='Пароль',
#                                 widget=forms.PasswordInput(attrs={'class': 'form-input'}))
#     password2 = forms.CharField(label='Подтверждение пароля',
#                                 widget=forms.PasswordInput(attrs={'class': 'form-input'}))

# class Meta:
#     model = User
#     fields = ('username', 'email', 'password1', 'password2')


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Почта', }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)
        self.fields['email'].widget.attrs.update({"required": True})
