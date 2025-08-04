from rest_framework import serializers
from apps.professionals.models import *



class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = [
            'id', 'name',
        ]


class SpecializationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = [
            'id', 'name'
        ]


class ProfessionalProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfessionalProfile
        fields = [
            "id", "fullname", "title", "profession", "specializations","bio", "years_of_experience", 
            "phone", "email", "website", "location", "profile_image", "banner_image", "consultation_fee"
        ]
        read_only_fields = ['id']

    


class ProfessionalProfileReadSerializer(serializers.ModelSerializer):

    professionname = serializers.SerializerMethodField()
    professionicon = serializers.SerializerMethodField()

    class Meta:
        model = ProfessionalProfile
        fields = [
            "id", "fullname", "title", "profession", "professionname", "professionicon", "specializations","bio", "years_of_experience", 
            "phone", "email", "website", "location", "profile_image", "banner_image", "consultation_fee", "slug"
        ]
        read_only_fields = ['id']


    def get_professionname(self, obj):
        if obj.profession:
            return obj.profession.name
        return None
    
    def get_professionicon(self, obj):
        if obj.profession:
            return obj.profession.icon
        return None

