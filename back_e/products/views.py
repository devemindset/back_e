
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

