# Generated by Django 5.2.4 on 2025-07-20 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0014_remove_businesshour_is_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesshour',
            name='closing_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='businesshour',
            name='opening_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
