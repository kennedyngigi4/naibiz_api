from django.urls import path
from apps.professionals.views import *

urlpatterns = [
    path( "all/", AllProfessionals.as_view(), name="all", ),
    path( "professions/", ProfessionsView.as_view(), name="professions", ),
    path( "professional/<slug:slug>/", ProfessionalDetailsView.as_view(), name="professional", ),
    path( "specializations/", SpecializationsView.as_view(), name="specializations", ),
    path( "profile/", ProfessionalProfileView.as_view(), name="profile", ),
]
