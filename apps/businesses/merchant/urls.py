from django.urls import path
from apps.businesses.merchant.views import *


urlpatterns = [
    path("add_listing/", AddListingView.as_view(), name="add_listing", ),
    path("all_listings/", AllListingsView.as_view(), name="all_listings", ),
]


