#  Copyright (c) Code Written and Tested by Ahmed Emad on 2019

# Generated by Django 3.0 on 2019-12-26 14:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('drivers', '0003_auto_20191225_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverprofilemodel',
            name='vehicle_type',
            field=models.CharField(max_length=20),
        ),
    ]
