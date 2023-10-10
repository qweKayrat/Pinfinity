from django import forms
from .models import Review, Content, Questions


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['image', 'title', 'content', 'source_link', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'source_link': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-input', 'rows': 10}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['body']

        widgets = {
            'body': forms.TextInput(attrs={'class': 'comment_input', 'placeholder': 'Добавить комментарий'}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['type', 'title', 'body', 'email']

        widgets = {
            # 'type': forms.Select(choices=[(key, value) for key, value in Questions.TYPE if key != Questions.PUBLISHED]),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': "Вопроса"}),
            'body': forms.Textarea(attrs={'class': 'form-input', 'rows': 10, 'placeholder': "Расскажите подробнее"}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Укажите почту на которую вам отправить '
                                                                                   'ответ'}),
        }
