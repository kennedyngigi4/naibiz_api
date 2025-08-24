from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import Lower

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


from apps.accounts.models import *
from apps.businesses.models import *
from apps.businesses.serializers import *
# Create your views here.


class PaginationView(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryListWithBusinessCountView(generics.ListAPIView):
    serializer_class = CategoryWithCountSerializer

    def get_queryset(self):
        return Category.objects.filter(is_main=True).annotate(business_count=Count("businesses")).order_by("-business_count")


class CategoriesView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by("name")


class SubCategoriesView(generics.ListAPIView):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all().order_by("name")


class HomeListingView(generics.ListAPIView):
    serializer_class = BusinessSerializer
    queryset = Business.objects.all().order_by("-created_at")

    def get_queryset(self):
        section = self.request.query_params.get("section")

        queryset = self.queryset

        if section in [ "popular", "featured", "environs", "top", "new" ]:
            queryset = queryset.filter(section=section)
        
        return queryset



class AllListingsView(generics.ListAPIView):
    serializer_class = BusinessSerializer
    queryset = Business.objects.all().order_by("-created_at")
    pagination_class = PaginationView
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']


class BusinessDetailsView(generics.RetrieveAPIView):
    serializer_class = BusinessSerializer
    queryset = Business.objects.all()
    lookup_field = "slug"



class SimilarBusinessView(generics.ListAPIView):
    serializer_class = BusinessSerializer
    queryset = Business.objects.all().order_by("-created_at")

    def get_queryset(self):
        category = self.request.query_params.get("category")
        return self.queryset.filter(category=category)


class ReviewsView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all().order_by("-created_at")

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Review submitted!"})
        return Response({ "success": False, "message": serializer.errors })




class SearchQueryView(generics.ListAPIView):
    serializer_class = BusinessSerializer

    def get_queryset(self):
        queryset = Business.objects.all()
        q = self.request.query_params.get("q")
        location = self.request.query_params.get("location")
        category = self.request.query_params.get("category")

        if q:
            queryset = queryset.annotate(name_lower=Lower("name")).filter(name_lower__icontains=q.lower())  # adjust fields
        if location:
            queryset = queryset.annotate(location_lower=Lower("location")).filter(location_lower__icontains=location.lower())
        if category:
            queryset = queryset.filter(category_id=category)  # if FK
            # queryset = queryset.filter(category__name__icontains=category) # if name string

        return queryset
