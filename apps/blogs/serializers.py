from rest_framework import serializers
from apps.blogs.models import *


class BlogSerializers(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "id", "slug", "title", "category", "content", "image", "author", "is_published", "created_at", "views"
        ]

    def get_author(self, obj):
        return obj.author.fullname



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id", "name", "email", "desc", "created_at"
        ]



class CompanyReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyReview
        fields = [
            "id", "title", "content", "client_name", "client_designation", "rate"
        ]



