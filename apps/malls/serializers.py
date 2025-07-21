from rest_framework import serializers
from apps.malls.models import *


class MallSerializer(serializers.ModelSerializer):
    listings_count = serializers.IntegerField()

    class Meta:
        model = Mall
        fields = [
            'id', "name", "floors", "stalls", "descriprion", "email", "phone", "website", "main_image", "listings_count"
        ]


