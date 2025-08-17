from django.urls import path
from apps.businesses.merchant.views import *


urlpatterns = [
    path("statistics/", StatisticsView.as_view(), name="statistics", ),
    path("reviews/", MyBusinessReviewView.as_view(), name="reviews", ),
    path("bookings/", MyBookingsViews.as_view(), name="bookings", ),
    path("messages/", MessagesView.as_view(), name="messages"),

    path("add_listing/", AddListingView.as_view(), name="add_listing", ),
    path("all_listings/", AllListingsView.as_view(), name="all_listings", ),
    path("listing/<slug:slug>/", ListingDetails.as_view(), name="listing", ),
    path("listing_update/<slug:slug>/", ListingUpdateAPIView.as_view(), name="listing_update", ),
    path("gallery/", MerchantUploadImageView.as_view(), name="gallery", ),

    path( "delete/<str:pk>/", DeleteBusinessView.as_view(), name="delete", ),
]


