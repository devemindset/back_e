from .models import Order
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer,OrderItemSerializer,OrderPostSerializer
from rest_framework.views import APIView
from products.models import Product,ProductCategory
from .models import Order,OrderItem 

class OrderAPIView(APIView):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = OrderPostSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        full_name = serializer.validated_data["full_name"]
        email = serializer.validated_data["email"]
        address = serializer.validated_data["address"]  # dict avec country, address, etc.
        total_amount = serializer.validated_data["total_amount"]
        items = serializer.validated_data["items"]
        phonenumber = serializer.validated_data["phonenumber"]
        user = serializer.validated_data.get("user", None)
        session_id = serializer.validated_data.get("session_id", None)

        try:
            order = Order.objects.create(
                full_name=full_name,
                email=email,
                country=address["country"],
                address=address["address"],
                apartment=address.get("apartment"),
                city=address["city"],
                state=address.get("state"),
                zip=address["zip"],
                phonenumber=phonenumber,
                total_amount=total_amount,
                user=user,
                session_id=session_id,
            )

            for item in items:
                product_category = ProductCategory.objects.get(id=item["product_category"])
                OrderItem.objects.create(
                    order=order,
                    product_category=product_category,
                    quantity=item["quantity"],
                    price=product_category.price,
                )

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderItemAPIView(APIView):
    def get(self, request, order_id):
        items = OrderItem.objects.filter(order_id=order_id)
        return Response(OrderItemSerializer(items, many=True).data, status=status.HTTP_200_OK)

