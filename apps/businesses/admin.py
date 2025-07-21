from django.contrib import admin

from apps.businesses.models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Business)
admin.site.register(BusinessKYCData)
admin.site.register(BusinessHour)
admin.site.register(BusinessGallery)
admin.site.register(Review)
