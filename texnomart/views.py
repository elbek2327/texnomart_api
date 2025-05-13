from django.shortcuts import render
from rest_framework import generics
from texnomart.models import Product,Category
from .serializers import ProductSerializer,CategorySerializer

# Create your views here.


class ProductListView(generics.ListAPIView):
    """Bu view All product hammasini chiqaradi API da"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    
class CategoryProductListView(generics.ListAPIView):
    """Bu view Categoryni all detailini chiqarish uchun"""
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        slug = self.kwargs['category_slug']
        try:
            category=Category.objects.get(slug=slug) 
            return Product.objects.filter(category=category)
        except Category.DoesNotExist: #agar yo'q bolsa
            return Product.objects.none()
              
class ProductByCategoryListView(generics.ListAPIView):
    """Productni category bilan chiqarish uchun"""
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    