from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from apps.accounts.models import *
from apps.professionals.models import *
from apps.professionals.serializers import *
# Create your views here.



class ProfessionsView(generics.ListAPIView):
    serializer_class = ProfessionSerializer
    queryset = Profession.objects.all().order_by("name")


class SpecializationsView(generics.ListAPIView):
    serializer_class = SpecializationsSerializer
    queryset = Specialization.objects.all().order_by("name")



class AllProfessionals(generics.ListAPIView):
    serializer_class = ProfessionalProfileReadSerializer
    queryset = ProfessionalProfile.objects.all().order_by("-created_at")


class ProfessionalDetailsView(generics.RetrieveAPIView):
    serializer_class = ProfessionalProfileReadSerializer
    queryset = ProfessionalProfile.objects.all()
    lookup_field = "slug"



class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({ "success": True, "message": "Message sent."})
        return Response({ "success": False, "message": "An error occured."})



class BookingProfessionalView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({ "success": True, "message": "Message sent."})
        return Response({ "success": False, "message": "An error occured."})










class ProfessionalProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfessionalProfileSerializer
    queryset = ProfessionalProfile.objects.all()
    permission_classes = [ IsAuthenticated ]
    parser_classes = [ MultiPartParser, FormParser ]

    def get_object(self):
        user = self.request.user
        try:
            return ProfessionalProfile.objects.get(user=user)
        except ProfessionalProfile.DoesNotExist:
            return Response("You are not registered as a professional.")




class AddListProfessionalEducation(generics.ListCreateAPIView):
    serializer_class = ProfessionalEducationSerializer
    queryset = Education.objects.all()
    permission_classes = [ IsAuthenticated ]

    def post(self, request):
        user = self.request.user
        serializer = ProfessionalEducationSerializer(data=request.data)
        professional = ProfessionalProfile.objects.get(user=user)
        if serializer.is_valid():
            serializer.save(
                user=user,
                professional=professional
            )

            return Response({ "success": True, "message": "Added successfully!"})


class DeleteProfessionalEducation(generics.DestroyAPIView):
    serializer_class = ProfessionalEducationSerializer
    queryset = Education.objects.all()
    permission_classes = [ IsAuthenticated ]



class AddListProfessionalExperience(generics.ListCreateAPIView):
    serializer_class = ProfessionalExperienceSerializer
    queryset = WorkExperience.objects.all()
    permission_classes = [ IsAuthenticated ]


    def post(self, request):
        user = self.request.user

        
        serializer = ProfessionalExperienceSerializer(data=request.data)
        professional = ProfessionalProfile.objects.get(user=user)

        if serializer.is_valid():
            serializer.save(
                user=user,
                professional=professional
            )

            return Response({ "success": True, "message": "Added successfully!"})
        return Response({ "success": False, "message": serializer.errors})


class DeleteProfessionalExperience(generics.DestroyAPIView):
    serializer_class = ProfessionalExperienceSerializer
    queryset = WorkExperience.objects.all()
    permission_classes = [ IsAuthenticated ]


class AddListScheduleView(generics.ListCreateAPIView):
    serializer_class = ProfessionalScheduleSerializer
    queryset = Schedule.objects.all()
    permission_classes = [ IsAuthenticated ]

    def post(self, request):
        user = self.request.user

        serializer = ProfessionalScheduleSerializer(data=request.data, context={"request": request.data})
        professional = ProfessionalProfile.objects.get(user=user)

        if serializer.is_valid():
            serializer.save(
                user=user,
                professional=professional
            )

            return Response({ "success": True, "message": "Added successfully!"})
        return Response({ "success": False, "message": serializer.errors})



class DeleteProfessionalSchedule(generics.DestroyAPIView):
    serializer_class = ProfessionalScheduleSerializer
    queryset = Schedule.objects.all()
    permission_classes = [ IsAuthenticated ]




class AllMyBookings(generics.ListAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    permission_classes = [ IsAuthenticated ]

    def get_queryset(self):
        try:
            user = self.request.user
            professional = ProfessionalProfile.objects.get(user=user)
            return Booking.objects.filter(professional=professional)
        except ProfessionalProfile.DoesNotExist:
            return Booking.objects.none()



class AllMyMessages(generics.ListAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [ IsAuthenticated ]

    def get_queryset(self):
        try:
            user = self.request.user
            professional = ProfessionalProfile.objects.get(user=user)
            return Message.objects.filter(professional=professional)
        except ProfessionalProfile.DoesNotExist:
            return Message.objects.none()



class ProfessionalStatistics(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        user = self.request.user
        professional = ProfessionalProfile.objects.get(user=user)

        messages_count = Message.objects.filter(professional=professional).count()
        bookings_count = Booking.objects.filter(professional=professional).count()

        return Response({
            "messages_count": messages_count,
            "bookings_count": bookings_count
        })


