import uuid
from django.conf import settings
from django.db import models

# Create your models here.


class AffiliateProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='affiliate_profile', on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True)
    clicks = models.PositiveIntegerField(default=0)
    registrations = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"{self.user.fullname} - {self.code}"


class Referral(models.Model):
    affiliate = models.ForeignKey(AffiliateProfile, on_delete=models.CASCADE, related_name="referrals")
    referred_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="referred_by")
    created_at = models.DateTimeField(auto_now_add=True)
    business_registered = models.BooleanField(default=False)
    commission_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0)


