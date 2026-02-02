from rest_framework import serializers
from apps.shop.models import *



class ProductSerializer(serializers.ModelSerializer):

    whatsapp = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "price", "main_image", "description", "business", "whatsapp"
        ]


    def get_whatsapp(self, obj):
        return obj.business.whatsapp



class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_image = serializers.ImageField(source="product.image", read_only=True)
    seller_name = serializers.CharField(source="seller.fullname", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_name",
            "product_image",
            "price",
            "quantity",
            "seller_name",
            "status",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "total_price",
            "status",
            "payment_status",
            "date_created",
            "items",
            "items_count",
        ]

    def get_items_count(self, obj):
        return obj.orderitem_set.count()


