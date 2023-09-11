from django import forms
from .models import *


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'

    class Meta:
        model = Content
        fields = ['image', 'title', 'content', 'source_link', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-input', 'rows': 10}),
            # 'cat': forms.(attrs={'class': 'form-input', 'rows': 16}),
            # 'images': forms.ImageField(attrs={'class': 'form-input'}),
        }
