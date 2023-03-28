from django.shortcuts import render

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
