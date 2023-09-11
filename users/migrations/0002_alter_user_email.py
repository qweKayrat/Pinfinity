# Generated by Django 4.2.3 on 2023-08-21 09:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(error_messages={'unique': 'Пользователь с такой почтой уже существует.'}, help_text='Максимальная длина имени пользователя не должна превышать 150 символов', max_length=150, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_email', message='В названии почты допускаются только английские буквы, цифры и основные символы.', regex='^[a-zA-Z0-9._%+-]+@[a-zA-Z]+\\.[a-zA-Z]{2,}$')], verbose_name='email'),
        ),
    ]