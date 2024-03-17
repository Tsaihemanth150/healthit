# Generated by Django 4.2.9 on 2024-02-28 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0014_plan_alerts_plan_care_staff_available_and_more'),
        ('staff', '0004_staff_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='members.member'),
        ),
    ]
