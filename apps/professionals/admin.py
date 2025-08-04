from django.contrib import admin
from apps.professionals.models import *
# Register your models here.

admin.site.register(Profession)
admin.site.register(Specialization)
admin.site.register(ProfessionalProfile)
admin.site.register(Education)
admin.site.register(WorkExperience)

