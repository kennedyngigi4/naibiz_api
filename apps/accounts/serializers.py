from rest_framework import serializers 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from apps.accounts.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'slug', 'fullname', 'email', 'phone', 'gender', 'role', 'profile_image', 'date_joined', 'is_active', 
            'is_verified', 'date_joined',
        ]





class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = { "password": { "write_only": True }}
        fields = [
            "email", "fullname", "phone", "password", "role"
        ]

    
    def create(self, validated_data):

        user = User.objects.create_user(
            email=validated_data["email"],
            fullname=validated_data["fullname"],
            phone=validated_data["phone"],
            password=validated_data["password"],
            role=validated_data["role"],
        )

        return user



class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except AuthenticationFailed as e:
            raise AuthenticationFailed({ "success": False, "message": e})

        user = self.user
        # access_token = data["access"]
        data["success"] = True
        data["id"] = self.user.id
        data["fullname"] = self.user.fullname
        data["email"] = self.user.email

        return data



