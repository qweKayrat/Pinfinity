# Generated by Django 4.2.5 on 2023-10-06 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_message_options_message_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='img',
            new_name='image',
        ),
    ]