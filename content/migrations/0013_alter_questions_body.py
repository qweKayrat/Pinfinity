# Generated by Django 4.2.5 on 2023-09-26 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0012_remove_questions_content_questions_body_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='body',
            field=models.TextField(blank=True, null=True, verbose_name='Контент'),
        ),
    ]
