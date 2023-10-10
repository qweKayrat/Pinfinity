from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Почта', }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)
        self.fields['email'].widget.attrs.update({"required": True})


class UserProfileForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)
    source_link = forms.URLField(widget=forms.URLInput(), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'img', 'source_link')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']

        widgets = {
            'body': forms.TextInput(attrs={'class': 'message_input', 'placeholder': 'Напишите сообщение'}),
        }
