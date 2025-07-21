from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed

from apps.accounts.models import *
from apps.accounts.serializers import *

# Create your views here.



class RegistrationView(APIView):
    serializer_class = RegistrationSerializer


    def post(self, request): 
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({ "success": True, "message": "Registration successful."}, status=status.HTTP_200_OK)
        else:
            return Response({ "success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


    def post(self, request, *args, **kwargs):
        print(request.data)
        try:
            response = super().post(request, *args, **kwargs)
            data = response.data
            return Response(data, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({ "success": False, "message": str(e) }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({ "success": False, "message": "An unexpected error occurred.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




