import json
import razorpay
from forex_python.converter import CurrencyRates

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
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
    print("Serializer not yet validated!")

    serializer = OrderSerializer(data=request.data)
    # print(serializer)
    if serializer.is_valid():
        rzp_secret = settings.RPZ_SECRET_KEY # secret key. Refer line 37
        rzp_public = settings.RPZ_PUBLIC_KEY # It is the public key for my account of razorpay
        paid_amount = int(sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items']))

        print("Serializer is validated!")
        print(paid_amount)
        try:
            

            client = razorpay.Client(auth=(rzp_public, rzp_secret))
            
            # somehow this simply returns a dictionary
            order_json = client.order.create({
                "amount" : (paid_amount*100),
                "currency" : "INR",
                "receipt" : "Order from Djackets"
            })
            # The multiplication with 100 is done because we can't serialiize decimals in a json file

            print(type(order_json))


            print("Order created")
            serializer.save(user=request.user, paid_amount=paid_amount, order_id=order_json["id"])

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    errors = serializer.errors
    for field, field_errors in errors.items():
        # Printing the field and its associated errors
        print(f"Errors for field '{field}': {field_errors}")

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
    

def validate_payment(request):
    data = json.loads(request.body)
    razorpay_payment_id = data['razorpay_payment_id']
    razorpay_order_id = data['razorpay_order_id']
    razorpay_signature = data['razorpay_signature']

    client = razorpay.Client(auth=(settings.RPZ_PUBLIC_KEY, settings.RPZ_SECRET_KEY))

    params_dict = {
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_signature': razorpay_signature
    }

    res = client.utility.verify_payment_signature(params_dict)

    print(res)

    return JsonResponse({'success': True})
