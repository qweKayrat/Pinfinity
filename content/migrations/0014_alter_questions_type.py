# Generated by Django 4.2.5 on 2023-09-26 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0013_alter_questions_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='type',
            field=models.SmallIntegerField(choices=[(0, 'Проблема регистрации/авторизации'), (1, 'Ошибка при работе с сайтом'), (2, 'Предложения по улучшению'), (3, 'Опубликовано')], default=0, verbose_name='тип вопроса'),
        ),
    ]