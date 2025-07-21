import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import *
from apps.businesses.models import *
# Create your models here.


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    content = models.TextField(verbose_name=_("message"))
    date_created = models.DateTimeField(auto_now_add=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, verbose_name=_("business"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner", verbose_name=_("owner"))
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender", verbose_name=_("sender"))

    def __str__(self):
        return f"Message to {self.user}"
    


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255, verbose_name=_("title"))
    message = models.TextField(verbose_name=_("message"))
    notification_type = models.CharField(max_length=255, default='general')
    created_at = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"Notification to {self.recipient.name}"



