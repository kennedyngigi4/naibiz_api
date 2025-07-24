from django.urls import path
from apps.messaging.views import *


urlpatterns = [
    path( "send_message/", SendMessageView.as_view(), name="send_message", ),
    path( "booking/", BookingView.as_view(), name="booking", ),
]



