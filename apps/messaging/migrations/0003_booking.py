# Generated by Django 5.2.4 on 2025-07-23 17:29

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0022_businessgallery_created_by'),
        ('messaging', '0002_alter_message_business_alter_message_sender_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('boking_date', models.DateField(null=True)),
                ('booking_time', models.TimeField(null=True)),
                ('booking_message', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='businesses.business', verbose_name='business')),
            ],
        ),
    ]
