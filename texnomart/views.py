from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
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


class CategoryListCreateView(generics.ListCreateAPIView):
    """hamma categoriyalar listi, categoriya yaratish uchun api dan"""
    queryset = Category.objects.all()    
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Malumotni oladi, Update, Delete qiladi"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser] #admin bolsa ozgartiradi
    lookup_field = 'slug'
    
# Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    """Create qilish va Read"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
    
class ProductRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[permissions.IsAdminUser]
    

    
