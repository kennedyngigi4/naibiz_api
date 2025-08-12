from django.db.models import Sum

from rest_framework import serializers
from apps.affiliates.models import AffiliateProfile, Referral



class ReferralSerializer(serializers.ModelSerializer):
    referred_username = serializers.CharField(source='referred_user.username')

    class Meta:
        model = Referral
        fields = ['referred_username', 'commission_earned', 'created_at']



class AffiliateProfileSerializer(serializers.ModelSerializer):

    earnings = serializers.SerializerMethodField()
    latest_referrals = serializers.SerializerMethodField()

    class Meta:
        model = AffiliateProfile
        fields = [ 'code', 'clicks', 'registrations', 'earnings', 'latest_referrals' ]

    def get_earnings(self, obj):
        total = obj.referrals.aggregate(total=Sum('commission_earned'))['total']
        return total or 0

    def get_latest_referrals(self, obj):
        latest = obj.referrals.filter(commission_earned__gt=0).order_by('-created_at')[:5]
        return ReferralSerializer(latest, many=True).data
