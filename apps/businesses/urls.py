from django.urls import path
from apps.businesses.views import *



urlpatterns = [
    path( "categories_business_count/", CategoryListWithBusinessCountView.as_view(), name="categories_business_count", ),
    path( "categories/", CategoriesView.as_view(), name="categories", ),
    path( "subcategories/", SubCategoriesView.as_view(), name="subcategories", ),
    path( "home/", HomeListingView.as_view(), name="home", ),
    path( "all/", AllListingsView.as_view(), name="all", ),
    path( "business/<slug:slug>/", BusinessDetailsView.as_view(), name="business", ),
    path( "review/", ReviewsView.as_view(), name="review", ),
    path( "similar_businesses/", SimilarBusinessView.as_view(), name="similar_businesses", ),
    path( "search/", SearchQueryView.as_view(), name="search", ),
]


