from django.urls import path, include
from order import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.OrdersList.as_view()),
    path('validate_payment/', views.validate_payment, name='validate_payment'),
]