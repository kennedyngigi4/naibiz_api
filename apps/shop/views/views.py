from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.shop.models import *
from apps.accounts.models import *
from apps.shop.serializers import *
# Create your views here.


class AllProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    

class ProductDetailsView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "slug"


