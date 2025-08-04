from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.accounts.models import *
from apps.professionals.models import *


@receiver(post_save, sender=User)
def create_professional(sender, instance, created, **kwargs):
    if created: 
        if instance.role == "professional":
            profile = ProfessionalProfile.objects.create(
                user=instance,
                fullname=instance.fullname
            )


