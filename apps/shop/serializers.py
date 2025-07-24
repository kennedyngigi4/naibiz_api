from rest_framework import serializers
from apps.shop.models import *



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id", "name", "price", "main_image", "description", "business"
        ]



