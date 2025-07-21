from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import *
from apps.businesses.models import *
from apps.businesses.serializers import *




class AddListingView(APIView):
    permission_classes = [ IsAuthenticated ]
    serializer_class = BusinessSerializer

    def post(self, request):
        user = self.request.user
        serializer = self.serializer_class(data=request.data, context={"request": request})

        hours_data = request.data["hours"]
        for hour in hours_data:
            print("Hour type:", type(hour))
            print("Hour raw:", hour)
        
        if serializer.is_valid():
            print(request.data["hours"])
            serializer.save(
                created_by=user
            )
            return Response({ "success": True, "message": "Listing successful", })
        
        print("Validation Errors:", serializer.errors)
        return Response({ "success": False, "message": serializer.errors, })
    


class AllListingsView(generics.ListAPIView):
    permission_classes = [ IsAuthenticated ]
    serializer_class = BusinessSerializer
    queryset = Business.objects.all().order_by("-created_at")


    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(created_by=user)
        return queryset



