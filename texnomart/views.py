from django.shortcuts import render
from rest_framework import generics
from texnomart.models import Product
from .serializers import ProductSerializer

# Create your views here.

def some():
    pass

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    