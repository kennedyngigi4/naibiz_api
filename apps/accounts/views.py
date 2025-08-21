from django.shortcuts import render
from django.contrib.auth import get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.models import *
from apps.accounts.serializers import *
from apps.affiliates.models import *

# Create your views here.

User = get_user_model()

class RegistrationView(APIView):
    serializer_class = RegistrationSerializer


    def post(self, request): 
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()

            # Check for referral cookie
            affiliate_code = request.COOKIES.get('affiliate_code')
            
            if affiliate_code:
                print(affiliate_code)
                try:
                    affiliate = AffiliateProfile.objects.get(code=affiliate_code)

                    if affiliate.user != user:
                        # Increment registrations count
                        affiliate.registrations += 1
                        affiliate.save()

                        # Record referral
                        Referral.objects.create(
                            affiliate=affiliate,
                            referred_user=user
                        )
                except AffiliateProfile.DoesNotExist:
                    pass  # invalid code, ignore

            return Response({ "success": True, "message": "Registration successful."}, status=status.HTTP_200_OK)
        else:
            return Response({ "success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


    def post(self, request, *args, **kwargs):
        
        try:
            response = super().post(request, *args, **kwargs)
            data = response.data
            return Response(data, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({ "success": False, "message": str(e) }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({ "success": False, "message": "An unexpected error occurred.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get("token")
        
        try:
            # VERIFY GOOGLE ID TOKEN
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), settings.GOOGLE_CLIENT_ID
            )

            email = idinfo["email"]

            user = User.objects.filter(email=email).first()
            if not user:
                return Response({
                    "success": False,
                    "message": "No account found. Please sign up first."
                }, status=status.HTTP_403_FORBIDDEN)
            

            
            # ISSUE jwt token
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "success": True,
                "id": user.id,
                "fullname": user.fullname,
                "email": user.email,
                "role": user.role,
            })


        except ValueError:
            return Response({
                "success": False,
                "message": "Invalid Google token"
            }, status=status.HTTP_400_BAD_REQUEST)




class ProfileView(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        user = self.request.user
        serializer = UserSerializer(user).data
        return Response(serializer)




class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [ IsAuthenticated ]


    def get_object(self):
        return self.request.user
    

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            "success": True,
            "message": "Profile updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


