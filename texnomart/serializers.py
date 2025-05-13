from rest_framework import serializers
from texnomart.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    """Product show all serializer"""
    category = serializers.SlugRelatedField(queryset = Category.objects.all(), slug_field = 'slug')

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('name','description','price','quantity','created_at','updated_at')
        
