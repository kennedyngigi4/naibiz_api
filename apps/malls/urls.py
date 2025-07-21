from django.urls import path
from apps.malls.views import *



urlpatterns = [
    path("all/", MallsView.as_view(), name="all", ),
]