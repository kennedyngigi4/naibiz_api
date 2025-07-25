from django.urls import path
from apps.shop.views import *



urlpatterns = [
    path( "all/", AllProductsView.as_view(), name="all", ),
    path( "product/<slug:slug>/", ProductDetailsView.as_view(), name="product", ),
]
