from django.urls import path
from apps.shop.merchant.views import *


urlpatterns = [
    path("upload_product/", UploadProductView.as_view(), name="upload_product", ),
    path("business_products/", BusinessProductsView.as_view(), name="business_products", ),
    path("delete-product/<str:pk>", DeleteProductView.as_view(), name="delete-product", ),
]

