# Generated by Django 4.2.9 on 2024-02-03 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_question'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='Member',
            new_name='member',
        ),
    ]
