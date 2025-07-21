from django.shortcuts import render
from django.db.models import Count

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import *
from apps.businesses.models import *
from apps.businesses.serializers import *
# Create your views here.


class CategoryListWithBusinessCountView(generics.ListAPIView):
    serializer_class = CategoryWithCountSerializer

    def get_queryset(self):
        return Category.objects.annotate(business_count=Count("businesses")).order_by("-business_count")


class CategoriesView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by("name")


class SubCategoriesView(generics.ListAPIView):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all().order_by("name")


class PopularListingView(generics.ListAPIView):
    serializer_class = BusinessSerializer
    queryset = Business.objects.all().order_by("-views")



class BusinessDetailsView(generics.RetrieveAPIView):
    serializer_class = BusinessSerializer
    queryset = Business.objects.all()
    lookup_field = "slug"

