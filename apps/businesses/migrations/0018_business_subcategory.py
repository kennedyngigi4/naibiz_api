# Generated by Django 5.2.4 on 2025-07-21 04:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0017_remove_business_geo_latlng_business_latitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='businesses.subcategory', verbose_name='subcategory'),
        ),
    ]
