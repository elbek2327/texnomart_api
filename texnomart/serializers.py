from rest_framework import serializers
from texnomart.models import Product, Category

#1 topshiriq
class ProductSerializer(serializers.ModelSerializer):
    """Product show all serializer"""
    category = serializers.SlugRelatedField(queryset = Category.objects.all(), slug_field = 'slug')

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_at','updated_at')
        
#2 topshiriq
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('slug',)

