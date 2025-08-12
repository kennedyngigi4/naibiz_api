from decimal import Decimal

from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.affiliates.models import Referral
from apps.businesses.models import Business, Category



@receiver(post_save, sender=Business)
def award_first_business_commission(sender, instance, created, **kwargs):
    if created:
        owner = instance.created_by
        category = instance.category
        print(category.price)
        if Business.objects.filter(created_by=owner).count() == 1:
            try:
                referral = Referral.objects.get(referred_user=owner)
                commission = Decimal(category.price) * Decimal('0.20')
                referral.commission_earned += commission
                referral.save()
            except Referral.DoesNotExist:
                pass

