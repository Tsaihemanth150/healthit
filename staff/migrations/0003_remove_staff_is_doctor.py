# Generated by Django 4.2.9 on 2024-02-07 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_staff_healthit_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='is_doctor',
        ),
    ]
