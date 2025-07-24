from rest_framework import serializers 
from apps.messaging.models import *


class MessageSerializer(serializers.ModelSerializer):

    businessname = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id", "business", "content", "businessname"
        ]

    def get_businessname(self, obj):
        return obj.business.name


class BookingSerializer(serializers.ModelSerializer):
    businessname = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            "id", "booking_date", "booking_time", "booking_message", "business", "businessname"
        ]


    def get_businessname(self, obj):
        return obj.business.name
