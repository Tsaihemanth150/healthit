# Generated by Django 4.2.9 on 2024-03-09 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0014_plan_alerts_plan_care_staff_available_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentRequset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Request_id', models.CharField(default='', editable=False, max_length=20, unique=True)),
                ('Desc', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('Time', models.TimeField()),
            ],
        ),
    ]