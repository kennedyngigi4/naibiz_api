from django.urls import path
from apps.businesses.views import *



urlpatterns = [
    path( "categories_business_count/", CategoryListWithBusinessCountView.as_view(), name="categories_business_count", ),
    path( "categories/", CategoriesView.as_view(), name="categories", ),
    path( "subcategories/", SubCategoriesView.as_view(), name="subcategories", ),
    path( "home/", HomeListingView.as_view(), name="home", ),
    path( "business/<slug:slug>/", BusinessDetailsView.as_view(), name="business", ),
]


