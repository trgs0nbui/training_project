from rest_framework import serializers
from .models import Product, Category, Tag

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category', 'description', 'tags']
        
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'description', 'tags']
        
    def valiate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero")
        return value
    
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Product name must be at least 3 characters")
        return value