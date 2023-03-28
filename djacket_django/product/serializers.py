# This script is used to fetch data from database and convert them to json format
# The converted JSON is then sent to the frontend for display.
# This is the whole function of serializers! These are embedded with django "rest_framework" library

from rest_framework import serializers
from .models import Product

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
            "get_thumbnail"
        )



