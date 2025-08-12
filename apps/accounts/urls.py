from django.urls import path
from apps.accounts.views import *



urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration", ),
    path("login/", LoginView.as_view(), name="login", ),

    path( "profile/", ProfileView.as_view(), name="profile", ),
    path( "profile-update/", UpdateProfileView.as_view(), name="profile-update"),
]

