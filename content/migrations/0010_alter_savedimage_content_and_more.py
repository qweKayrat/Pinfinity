# Generated by Django 4.2.5 on 2023-09-21 06:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0009_alter_savedimage_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedimage',
            name='content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_images', to='content.content', verbose_name='Изображение'),
        ),
        migrations.AlterUniqueTogether(
            name='savedimage',
            unique_together={('user', 'content')},
        ),
    ]
