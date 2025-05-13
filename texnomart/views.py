from django.shortcuts import render
from rest_framework import generics,  permissions, status 
from django.contrib.auth.models import User
from texnomart.models import Product,Category, Korzinka, Comment
from .serializers import (ProductSerializer,
                          CategorySerializer,
                          KorzinkaSerializer,
                          LoginSerializer,
                          RegisterSerializer,
                          CommentSerializer)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny
from config.caching import get_cached_log, cache_log

#Authentication Views
class RegisterApiView(generics.CreateAPIView):
    """Registering user"""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
    
class LoginApiView(APIView):
    """Login view"""
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user) 
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    """
    User Logout uchun view
    """
    def post(self, request):
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
            logout(request) # built-in logout
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Not logged in'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
            logout(request)
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Not logged in'}, status=status.HTTP_400_BAD_REQUEST)
         

#Kategoriyalar
class CategoryProductListView(generics.ListAPIView):
    """Bu view Categoryni all detailini chiqarish uchun"""
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        slug = self.kwargs['category_slug']
        try:
            category=Category.objects.get(slug=slug) 
            return Product.objects.filter(category=category)
        except Category.DoesNotExist: #agar yo'q bolsa
            return Product.objects.none()

class CategoryListCreateView(generics.ListCreateAPIView):
    """hamma categoriyalar listi, categoriya yaratish uchun api dan"""
    queryset = Category.objects.all()    
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Malumotni oladi, Update, Delete qiladi"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser] #admin bolsa ozgartiradi # permission kerak login uchun
    lookup_field = 'slug'

# Product Views    
class ProductListView(generics.ListAPIView):
    """Bu view All product hammasini chiqaradi API da"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductByCategoryListView(generics.ListAPIView):
    """Productni category bilan chiqarish uchun"""
    queryset=Product.objects.all()
    serializer_class=ProductSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    """Create qilish va Read"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
    
class ProductRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """bu delete va update uchun view"""
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[permissions.IsAdminUser] # permission kerak login uchun


#Korzinka
class KorzinkaListView(generics.ListAPIView):
    """Bu korzinkani ozi uchun hammasini chiqaruvchi view"""
    queryset = Korzinka.objects.all()
    serializer_class = KorzinkaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class KorzinkaListCreateView(generics.CreateAPIView):
    """Bu korzinkaga user product add qilishi uchun"""
    queryset = Korzinka.objects.all()
    serializer_class = KorzinkaSerializer #permission yozish kk login uchun
    permission_classes = [permissions.IsAuthenticated]
    
class KorzinkaRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Korzinka edit product"""
    queryset = Korzinka.objects.all()
    serializer_class = KorzinkaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
#Comment views
class CommentListView(generics.ListAPIView):
    """Hamma yozilgan commentlar"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentCreateView(generics.CreateAPIView):
    """Addind comment to a product"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """UPDATE and DElete comment by id"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

#Caching
class CachedProductListView(generics.ListAPIView):
    """Caching"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        cached_products = get_cached_log('all_products')
        if cached_products:
            return cached_products
        else:
            products = Product.objects.all()
            cache_log('all_products', products)
            return products

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)