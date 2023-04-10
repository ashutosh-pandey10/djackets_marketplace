from django.http import Http404

# Create your views here.
from .serializers import ProductSerializer
from .models import Product

from rest_framework.views import APIView
from rest_framework.response import Response


class LatestProductList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4] # use of "manager" as .objects()
        serializer = ProductSerializer(products, many=True) # "many" has been set as True as there are multiple values associated with instance "product"

        return Response(serializer.data)

class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
            # "category__slug" means filtering out records in product with a category that has a slug value equal to passed argument.
        
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)

        return Response(serializer.data)
