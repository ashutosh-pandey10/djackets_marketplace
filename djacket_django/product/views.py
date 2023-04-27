from django.http import Http404

# Create your views here.
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view


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


class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)



@api_view(['POST'])
def search(request):
    query = request.data.get("query", "") # This empty string is the default value given to the incoming json with key as "query". In case if the "query" 
                                          # key is not present or the value ""(empty string) will be returned to the request
    if query:
        products = Product.objects.filter(Q(name__icontains=query) or Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)                  
    
    else:
        return Response({"products" : []})

