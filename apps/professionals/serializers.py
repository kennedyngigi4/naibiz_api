from rest_framework import serializers
from apps.professionals.models import *



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "id", "professional", "message", "created_at"
        ]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id","time_booked", "date_booked", "professional", "message", "created_at"
        ]


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
            "phone", "email", "website", "location", "latitude", "longitude", "profile_image", "banner_image", "consultation_fee"
        ]
        read_only_fields = ['id']



class ProfessionalEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            'id', 'institution', 'degree', 'field_of_study', 'start_year', 'end_year'
        ]


class ProfessionalExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = [
            'id', 'position', 'company', 'start_date', 'end_date', 'description'
        ]


class ProfessionalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = [
            'id', 'schedule_day', 'details', 'time_from', 'time_to'
        ]


class ProfessionalProfileReadSerializer(serializers.ModelSerializer):

    professionname = serializers.SerializerMethodField()
    professionicon = serializers.SerializerMethodField()
    education = ProfessionalEducationSerializer(many=True, required=False)
    work_experience = ProfessionalExperienceSerializer(many=True, required=False)
    schedule = ProfessionalScheduleSerializer(many=True, required=False)

    class Meta:
        model = ProfessionalProfile
        fields = [
            "id", "fullname", "title", "profession", "professionname", "professionicon", "specializations","bio", "years_of_experience", 
            "phone", "email", "website", "location", "latitude", "longitude", "profile_image", "banner_image", "consultation_fee", "slug", "education", "work_experience", "schedule"
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

