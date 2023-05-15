import stripe
from forex_python.converter import CurrencyRates

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer



@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        stripe.api_key = settings.STRIPE_SECRET_KEY # secret key. Refer line 37
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])

        # print("Serializer is validated!")

        try:
            charge = stripe.Charge.create(
                amount=int((paid_amount * conversion_ratio("INR", "USD")) * 100), #Stripe takes value in cents not dollars, hence the multiplication with 100.
                # The paid amount is converted to USD using the function, which is later converted to cents.
                currency='usd', # Stripe doesn't accept INR as a currency value, will later convert it to INR by multiplying by 80(assumed current price USD to INR)
                description='Charge from Djackets',
                source=serializer.validated_data['stripe_token'] # This we get fro the frontend. It is the public key for my account of stripe
            )

            print("charge created")
            serializer.save(user=request.user, paid_amount=paid_amount)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
    

def conversion_ratio(base_currency : str, destination_currency : str) -> float:
    
    conversion_rate = CurrencyRates()
    ratio = conversion_rate.get_rate(base_currency, destination_currency)

    return ratio
