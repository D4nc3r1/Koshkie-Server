#  Copyright (c) Code Written and Tested by Ahmed Emad in 05/02/2020, 14:19

# Generated by Django 3.0.3 on 2020-02-05 12:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('shops', '0031_auto_20200204_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopaddressmodel',
            name='city',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='shopaddressmodel',
            name='country',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
