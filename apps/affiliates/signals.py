from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.conf import settings
from apps.affiliates.models import AffiliateProfile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_affiliate_profile(sender, instance, created, **kwargs):
    if created:
        code = get_random_string(8)
        AffiliateProfile.objects.create(user=instance, code=code)


