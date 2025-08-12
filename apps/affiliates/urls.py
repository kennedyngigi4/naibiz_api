from django.urls import path
from apps.affiliates.views import *


urlpatterns = [
    path( "click/<str:code>/", TrackClickView.as_view(), name="track-click", ),
]



urlpatterns += [
    # logged in user affliate links
    path("profile/", MyAffiliateProfile.as_view(), name="profile", ),
]


