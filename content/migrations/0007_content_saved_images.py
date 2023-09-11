# Generated by Django 4.2.3 on 2023-08-29 09:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0006_alter_questions_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='saved_images',
            field=models.ManyToManyField(blank=True, related_name='saved', to=settings.AUTH_USER_MODEL, verbose_name='Сохраненные изображения'),
        ),
    ]
