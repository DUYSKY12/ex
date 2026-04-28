from rest_framework import serializers
from .models import Product, Category, Book, Electronics, Fashion

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Book
        fields = '__all__'

class ElectronicsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Electronics
        fields = '__all__'

class FashionSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Fashion
        fields = '__all__'