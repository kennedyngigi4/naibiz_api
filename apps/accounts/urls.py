from django.urls import path
from apps.accounts.views import *



urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration", ),
    path("login/", LoginView.as_view(), name="login", ),
]

