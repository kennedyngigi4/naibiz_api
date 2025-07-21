from django.shortcuts import render
from django.db.models import Count

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.accounts.models import User
from apps.businesses.models import *
from apps.malls.models import *
from apps.malls.serializers import *
# Create your views here.




class MallsView(generics.ListAPIView):
    serializer_class = MallSerializer
    queryset = Mall.objects.all().order_by("name")
    
    def get_queryset(self):
        return Mall.objects.annotate(listings_count=Count("business_malls"))




