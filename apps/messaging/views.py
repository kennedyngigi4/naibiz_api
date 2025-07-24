from django.shortcuts import render


from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import *
from rest_framework.response import Response

from apps.messaging.models import *
from apps.messaging.serializers import *
# Create your views here.



class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({ "success": True, "message": "Message sent successfully!"})
        return Response({ "success": False, "message": serializer.errors})




class BookingView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()


    def post(self, request):

        serializer = BookingSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            
            serializer.save()
            return Response({ "success": True, "message": "Booking sent successfully!"})
        return Response({ "success": False, "message": serializer.errors})




