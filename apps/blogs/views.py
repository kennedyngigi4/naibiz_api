from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import *
from apps.blogs.models import *
from apps.blogs.serializers import *
# Create your views here.



class BlogsView(generics.ListAPIView):
    serializer_class = BlogSerializers
    queryset = Blog.objects.all().order_by("-created_at")


class BlogDetailsView(generics.RetrieveAPIView):
    serializer_class = BlogSerializers
    queryset = Blog.objects.all()
    lookup_field = "slug"


class CommentsView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all().order_by("-created_at")
    

class CompanyReviewsView(generics.ListAPIView):
    serializer_class = CompanyReviewSerializer
    queryset = CompanyReview.objects.all().order_by("?")


