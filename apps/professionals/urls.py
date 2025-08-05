from django.urls import path
from apps.professionals.views import *

urlpatterns = [
    path( "all/", AllProfessionals.as_view(), name="all", ),
    path( "professions/", ProfessionsView.as_view(), name="professions", ),
    path( "professional/<slug:slug>/", ProfessionalDetailsView.as_view(), name="professional", ),
    path( "specializations/", SpecializationsView.as_view(), name="specializations", ),
    path( "profile/", ProfessionalProfileView.as_view(), name="profile", ),
    path( "education/", AddListProfessionalEducation.as_view(), name="education", ),
    path( "education-delete/<str:pk>/", DeleteProfessionalEducation.as_view(), name="education-delete", ),
    path( "experience/", AddListProfessionalExperience.as_view(), name="experience", ),
    path( "experience-delete/<str:pk>/", DeleteProfessionalExperience.as_view(), name="experience-delete", ),
    path( "schedule/", AddListScheduleView.as_view(), name="schedule", ),
    path( "schedule-delete/<str:pk>/", DeleteProfessionalSchedule.as_view(), name="schedule-delete", ),
]
