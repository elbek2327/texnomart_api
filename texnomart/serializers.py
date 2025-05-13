from rest_framework import serializers
from texnomart.models import Product, Category, Korzinka, Comment
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
# from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#User serializers
User = get_user_model()

class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(LoginSerializer, cls).get_token(user)
        token['username']=user.username
        return token
    
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
        

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_staff = True)
        user.set_password(validated_data['password'])
        user.save()
        return user

#Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    """Product show all serializer"""
    category = serializers.SlugRelatedField(queryset = Category.objects.all(), slug_field = 'slug')

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_at','updated_at')
        
#Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('slug',)

#Korzinka Serializer
class KorzinkaSerializer(serializers.ModelSerializer):
    """Korzinka modeli uchun serializer"""
    product = serializers.SlugRelatedField(queryset = Product.objects.all(), slug_field = 'name') # Productni ham olish uchn
    user = serializers.SlugRelatedField(queryset = User.objects.all(), slug_field = 'username' ) # userni korzinka listga chiqarish uchun
    class Meta:
        model = Korzinka
        fields = ('id','user', 'product', 'quantity','created_at')
        read_only_files = ('created_at',)

#Comment Serializers
class CommentSerializer(serializers.ModelSerializer):
    """Comment uchun serializer"""
    user = serializers.SlugRelatedField(queryset = User.objects.all(), slug_field = 'username')
    product = serializers.SlugRelatedField(queryset = Product.objects.all(), slug_field = 'name')
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_files = ('created_at',)
        