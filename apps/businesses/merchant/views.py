from django.shortcuts import render, get_object_or_404
from decimal import Decimal

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from apps.accounts.models import *
from apps.affiliates.models import Referral
from apps.businesses.models import *
from apps.businesses.serializers import *
from apps.messaging.serializers import *
from apps.payments.mpesa import *


class StatisticsView(APIView):

    def get(self, request):
        businesses_count = Business.objects.filter(created_by=self.request.user).count()
        bookings_count = Booking.objects.filter(business__created_by=self.request.user).count()
        reviews_count = Review.objects.filter(business__created_by=self.request.user).count()
        messages_count = Message.objects.filter(business__created_by=self.request.user).count()

        return Response([
            { "title": "businesses", "count": businesses_count, "bg": "bg-light-success", "icon": "BsPinMapFill", "iconStyle":'text-success', },
            { "title": "bookings", "count": bookings_count, "bg": "bg-light-danger", "icon": "BsGraphUpArrow", "iconStyle":'text-danger', },
            { "title": "reviews", "count": reviews_count, "bg": "bg-light-warning", "icon": "BsSuitHeart", "iconStyle":'text-warning', },
            { "title": "messages", "count": messages_count, "bg": "bg-light-info", "icon": "BsYelp", "iconStyle":'text-info', },
        ])


class AddListingView(APIView):
    permission_classes = [ IsAuthenticated ]
    serializer_class = BusinessSerializer

    def post(self, request):
        # 1. Create the business
        user = self.request.user
        serializer = self.serializer_class(data=request.data, context={"request": request})
        
        if serializer.is_valid():
            category = request.data["category"]
            phone = request.data["phone"]
            category = get_object_or_404(Category, id=category)
            business = serializer.save(
                created_by=user
            )

            if business:
                # 2. Mpesa 
                MPESA(phone, int(category.price)).MpesaSTKPush()
                return Response({ "success": True, "message": "Listing successful", })
        
        print("Validation Errors:", serializer.errors)
        return Response({ "success": False, "message": serializer.errors, })
    


class AllListingsView(generics.ListAPIView):
    permission_classes = [ IsAuthenticated ]
    serializer_class = BusinessSerializer
    queryset = Business.objects.all().order_by("-created_at")


    def get_queryset(self):
        
        
        user = self.request.user
        queryset = self.queryset.filter(created_by=user)
        return queryset


class ListingDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [ IsAuthenticated ]
    serializer_class = BusinessSerializer
    queryset = Business.objects.all()
    lookup_field = "slug"



class ListingUpdateAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request, slug):

        business = get_object_or_404(Business, slug=slug)
        serializer = BusinessSerializer(business, data=request.data, context={"request": request }, partial=True)
        print(type(request.FILES.get("profile_image"))) 
        if serializer.is_valid():
            print(business)
            serializer.save()
            return Response({'success': True, 'message': 'Listing updated successfully.'})
        print(serializer.errors)
        return Response({'success': False, 'message': serializer.errors}, status=400)




class MerchantUploadImageView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GallerySerializer
    queryset = BusinessGallery.objects.all()

    def get_queryset(self):
        queryset = BusinessGallery.objects.filter(created_by=self.request.user)
        business_id = self.request.query_params.get('business')

        if business_id:
            queryset = queryset.filter(business_id=business_id)
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    
        





class MyBookingsViews(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [ IsAuthenticated ]

    def get_queryset(self):
        return Booking.objects.filter(business__created_by=self.request.user)


class MyBusinessReviewView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [ IsAuthenticated ]


    def get_queryset(self):
        return Review.objects.filter(business__created_by=self.request.user)



class MessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [ IsAuthenticated ]

    def get_queryset(self):
        return Message.objects.filter(business__created_by=self.request.user)
    




class DeleteBusinessView(generics.DestroyAPIView):
    serializer_class = BusinessSerializer
    queryset = Business.objects.all()
    permission_classes = [ IsAuthenticated ]
    

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        business_name = instance.name  
        self.perform_destroy(instance)

        return Response({
                "status": "success",
                "message": f"Business '{business_name}' deleted successfully.",
                "deleted_id": kwargs.get("id"),
            },
            status=status.HTTP_200_OK
        )


