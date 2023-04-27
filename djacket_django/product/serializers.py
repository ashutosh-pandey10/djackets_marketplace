# This script is used to fetch data from database and convert them to json format
# The converted JSON is then sent to the frontend for display.
# This is the whole function of serializers! These are embedded with django "rest_framework" library

from rest_framework import serializers
from .models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "description",
            "price",
            "get_image",
            "get_thumbnail",
        )


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    # Above object holds all the products along with their details
    
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products",
        )

