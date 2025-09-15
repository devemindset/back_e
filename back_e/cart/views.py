from rest_framework.views import APIView
from .models import Cart,CartItem
from rest_framework.response import Response
from .serializers import CartSerializer,CartItemSerializer,CreateCartItemSerializer
from rest_framework import status
from products.models import Product

class CartAPIView(APIView):
    def get(self, request, session_id):
        try:
            cart = Cart.objects.get(session_id=session_id)

            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data.get("user",None)

        try:
            cart, created = Cart.objects.get_or_create(
                user=user
            )
            status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return Response(CartSerializer(cart).data, status=status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CartItemAPIView(APIView):
    def get(self, request, cart_id):
        items = CartItem.objects.filter(cart_id=cart_id)
        return Response(CartItemSerializer(items, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateCartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        cart = serializer.validated_data["cart"]
        product_category = serializer.validated_data["product_category"]
        quantity = serializer.validated_data.get("quantity", 1)

        try:
            item, created = CartItem.objects.get_or_create(
                cart=cart,
                product_category=product_category,
                defaults={"quantity": quantity}
            )
            if not created:
                item.quantity = quantity
                item.save()

            status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return Response(CartItemSerializer(item).data, status=status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, cart_item_id):
        try:
            item = CartItem.objects.get(id=cart_item_id)
            item.delete()
            return Response({"message": "Cart item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
