import json
from rest_framework import serializers 
from apps.accounts.models import User
from apps.businesses.models import *
from django.utils import timezone
from django.contrib.auth import get_user_model


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'fullname', 'profile_image',
        ]


class CategoryWithCountSerializer(serializers.ModelSerializer):
    business_count = serializers.IntegerField()

    class Meta:
        model = Category
        fields = [
            'id','name', 'icon', 'business_count'
        ]



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id','name', 'price', 'date_created', 'icon'
        ]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = [
            'id','name', 'category'
        ]


class BusinessHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessHour
        fields = [
            'day', 'opening_time', 'closing_time',
        ]



class BusinessSerializer(serializers.ModelSerializer):
    hours = BusinessHourSerializer(many=True, required=False)
    is_open = serializers.SerializerMethodField()
    created_by = OwnerSerializer(read_only=True)
    category_name = serializers.SerializerMethodField()
    category_icon = serializers.SerializerMethodField()
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Business
        fields = [
            'id', 'slug', 'name', 'category', 'category_name', 'category_icon', 'mall', 'services', 'location', 'latitude', 'longitude', 'description', "profile_image", "main_banner", 
            'phone', 'email', 'website', 'whatsapp', 'facebook', 'instagram', 'twitterx', 'tiktok', 'linkedin', 'youtube',
            'is_verified', 'is_active', 'created_by', 'created_at', 'updated_at', 'expires_at', 'hours', 'views', 'is_open'
        ]
        read_only_fields = [ 'slug', 'created_at', 'updated_at', 'views' ]


    def get_is_open(self, obj):
        now = timezone.localtime()
        current_day = now.strftime('%a')
        current_time = now.time()

        today_hours = obj.hours.filter(day__iexact=current_day)
        for hour in today_hours:
            if hour.opening_time and hour.closing_time:
                if hour.opening_time <= current_time <= hour.closing_time:
                    return True
        return False


    def get_category_name(self, obj):
        return obj.category.name
    

    def get_category_icon(self, obj):
        return obj.category.icon


    def create(self, validated_data):
        request = self.context.get("request")
        # categories = validated_data.pop("category")
        business = Business.objects.create(**validated_data)
        # business.category.set(categories)

        hours_data = request.data.getlist("hours")  # ✅ returns a list
        for hour_str in hours_data:
            try:
                hour = json.loads(hour_str)
            except json.JSONDecodeError:
                continue
            if isinstance(hour, dict) and (hour.get("opening_time") or hour.get("closing_time")):
                BusinessHour.objects.create(business=business, **hour)
        
        return business

    
    def update(self, instance, validated_data):
        hours_data = validated_data.pop("hours", None)
        categories = validated_data.pop("category", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if categories is not None:
            instance.category.set(categories)

        if hours_data is not None:
            instance.hours.all().delete()
            for hour in hours_data:
                BusinessHour.objects.create(busness=instance, **hour)

        return instance