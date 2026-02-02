from django.urls import path
from apps.shop.views.views import *
from apps.shop.views.customer_views import *


urlpatterns = [
    path( "all/", AllProductsView.as_view(), name="all", ),
    path( "product/<slug:slug>/", ProductDetailsView.as_view(), name="product", ),
]


urlpatterns += [
    path( "place-order/", CreateOrderAPIView.as_view(), name="place-order" ),
    path( "customer-orders/", CustomerOrderListAPIView.as_view(), name="customer-orders" ),
]
