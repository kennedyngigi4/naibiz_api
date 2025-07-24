from django.urls import path
from apps.blogs.views import *


urlpatterns = [
    path( "blogs/", BlogsView.as_view(), name="blogs", ),
    path( "blog/<slug:slug>/", BlogDetailsView.as_view(), name="blog", ),
    path( "comments/", CommentsView.as_view(), name="comments", ),
    path( "company_reviews/", CompanyReviewsView.as_view(), name="company_reviews", ), 
]
