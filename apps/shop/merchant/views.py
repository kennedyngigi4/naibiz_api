from django.shortcuts import render


from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import *

from apps.accounts.models import *
from apps.businesses.models import *
from apps.shop.models import *
from apps.shop.serializers import *



class UploadProductView(APIView):
    permission_classes = [ IsAuthenticated ]
    serializer_class = ProductSerializer

    def post(self, request):
        user= self.request.user
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=user)
            return Response({ "success": True, "message": "Upload successful!"})
        return Response({ "success": False, "message": serializer.errors })



class BusinessProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [ IsAuthenticated ]


    def get_queryset(self):
        user = self.request.user
        business = self.request.query_params.get("business")
        queryset = Product.objects.filter(created_by=user, business=business)
        return queryset



class DeleteProductView(generics.DestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [ IsAuthenticated ]


    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        product_name = instance.name
        self.perform_destroy(instance)

        return Response({
            "status": "success",
            "message": f"Product '{product_name}' deleted successfully.",
            "deleted_id": kwargs.get("id"),
        }, status=status.HTTP_200_OK)



