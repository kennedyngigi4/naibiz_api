from rest_framework import serializers
from apps.shop.models import *



class ProductSerializer(serializers.ModelSerializer):

    whatsapp = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "price", "main_image", "description", "business", "slug", "whatsapp"
        ]


    def get_whatsapp(self, obj):
        return obj.business.whatsapp



