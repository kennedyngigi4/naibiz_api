import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import *
from apps.businesses.models import *
# Create your models here.



class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    booking_date = models.DateField(null=True)
    booking_time = models.TimeField(null=True)
    booking_message = models.TextField(null=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="bookings", verbose_name=_("business"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking_date} for {self.business.name}"
    


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    content = models.TextField(verbose_name=_("message"))
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="messages", verbose_name=_("business"))

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="owner", verbose_name=_("owner"))
    sender = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="sender", verbose_name=_("sender"))
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Message to {self.business.name}"
    


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255, verbose_name=_("title"))
    message = models.TextField(verbose_name=_("message"))
    notification_type = models.CharField(max_length=255, default='general')
    created_at = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"Notification to {self.recipient.name}"



