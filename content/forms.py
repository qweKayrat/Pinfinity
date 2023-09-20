from django import forms
from .models import *


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Content
        fields = ['image', 'title', 'content', 'source_link', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'source_link': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-input', 'rows': 10}),
        }
