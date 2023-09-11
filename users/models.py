from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_.!-]+$',
        message='В имени пользователя допускаются только английские буквы, цифры и основные символы.',
        code='invalid_username'
    )
    email_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z]+\.[a-zA-Z]{2,}$',
        message='Введите корректный email адрес.',
        code='invalid_email'
    )

    img = models.ImageField(upload_to='User/&Y/%m/%d/', blank=True, default="User/default.png", verbose_name='Изображение '
                                                                                                             'пользователя')
    source_link = models.URLField(max_length=200, blank=True, null=True, verbose_name='Ссылка для продвижения')
    username = models.CharField(_('username'), max_length=150, unique=True,
                                help_text=_('Максимальная длина имени пользователя не должна превышать 150 символов'),
                                validators=[username_validator],
                                error_messages={'unique': _("Пользователь с таким именем уже существует.")}, )
    email = models.CharField(_('email'), max_length=150, unique=True,
                             help_text=_('Максимальная длина имени пользователя не должна превышать 150 символов'),
                             validators=[email_validator],
                             error_messages={'unique': _("Пользователь с такой почтой уже существует.")}, )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = 'Пользователи'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.username})


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="messages")
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}"

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = 'Сообщения'
        ordering = ['is_read', '-created']

    def get_absolute_url(self):
        return reverse('profile', kwargs={'sender': self.sender})
