from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = ''
admin.site.site_title = ''

urlpatterns = [
    path('admin/', admin.site.urls),
    path( "api/account/", include("apps.accounts.urls")),


    path( "api/businesses/", include("apps.businesses.urls")),
    path( "api/businesses/merchant/", include("apps.businesses.merchant.urls")),


    path( "api/messages/", include("apps.messaging.urls")),


    path( "api/malls/", include("apps.malls.urls")),
]


urlpatterns += [
    path( "api/shop/merchant/", include("apps.shop.merchant.urls")),
]



urlpatterns += [
    path( "api/blogs/", include("apps.blogs.urls")),
]



urlpatterns += static( settings.STATIC_URL, document_root=settings.STATIC_ROOT )
urlpatterns += static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
