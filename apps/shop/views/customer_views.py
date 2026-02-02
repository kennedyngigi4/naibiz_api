from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from django.db import transaction

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.shop.models import *
from apps.shop.serializers import *

class CreateOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        print(request.data)


        cart = request.data.get("cart", [])
        phone = request.data.get("mpesaphone")

        if not cart:
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        total = Decimal("0.00")

        # 1️⃣ Create empty order
        order = Order.objects.create(
            user=request.user,
            total_price=0,
            payment_status="pending",
            status="pending",
        )

        # 2️⃣ Create order items
        for item in cart:
            product = Product.objects.select_for_update().get(id=item["id"])

            line_total = product.price * item["quantity"]
            total += line_total

            OrderItem.objects.create(
                order=order,
                product=product,
                seller=product.created_by,
                price=product.price,
                quantity=item["quantity"],
                status="pending",
            )

        # 3️⃣ Update total
        order.total_price = total
        order.save()

        # 4️⃣ Initiate Mpesa
        # checkout_id = initiate_stk_push(
        #     phone=phone,
        #     amount=int(total),
        #     account_reference=order.order_number,
        # )

        # order.mpesa_checkout_request_id = checkout_id
        order.save()

        return Response(
            {
                "success": True,
                "order_id": order.id,
                "order_number": order.order_number,
                "total": total,
                "message": "Enter your M-Pesa PIN to complete payment",
            },
            status=status.HTTP_201_CREATED
        )




class CustomerOrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = (
            Order.objects
            .filter(user=request.user)
            .prefetch_related("orderitem_set")  # count() is cheap, still prefetch to avoid N+1
            .order_by("-date_created")
        )
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)





