from django.shortcuts import render, get_object_or_404


from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.affiliates.models import AffiliateProfile
from apps.affiliates.serializer import *
# Create your views here.


class TrackClickView(APIView):

    def get(self, request, *args, **kwargs):
        code = kwargs.get('code')
        try: 
            affiliate = AffiliateProfile.objects.get(code=code)
            affiliate.clicks += 1
            affiliate.save()

            response = Response({ "success": True, "message": "Click tracked"})
            response.set_cookie(
                'affiliate_code',
                code,
                max_age=60*60*24*30, #30 days
                httponly=True,
                secure=True,
                samesite='None'
            )
            return response
        
        except AffiliateProfile.DoesNotExist:
            return Response({ "success": False, "message": "Invalid affiliate code"}, status=status.HTTP_404_NOT_FOUND)






# Afilliate Owner Functions

class MyAffiliateProfile(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        user = self.request.user

        profile = AffiliateProfile.objects.get(user=user)
        serializer = AffiliateProfileSerializer(profile)
        return Response(serializer.data)






