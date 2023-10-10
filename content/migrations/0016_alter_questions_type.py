# Generated by Django 4.2.5 on 2023-09-26 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0015_questions_email_alter_questions_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='type',
            field=models.SmallIntegerField(choices=[(0, 'Проблема регистрации/авторизации'), (1, 'Ошибка при работе с сайтом'), (2, 'Предложения по улучшению')], default=0, verbose_name='тип вопроса'),
        ),
    ]
