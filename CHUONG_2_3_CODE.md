# Chương 2.3.2 - Model tổng quát và Chi tiết theo Domain

## product-service/models.py

```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Book(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.product.name} by {self.author}"

class Electronics(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    warranty = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.brand}"

class Fashion(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.product.name} - {self.size} {self.color}"
```

## product-service/serializers.py

```python
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
```

## product-service/views.py

```python
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product, Category, Book, Electronics, Fashion
from .serializers import ProductSerializer, CategorySerializer, BookSerializer, ElectronicsSerializer, FashionSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        product = self.get_object()
        if hasattr(product, 'book'):
            serializer = BookSerializer(product.book)
        elif hasattr(product, 'electronics'):
            serializer = ElectronicsSerializer(product.electronics)
        elif hasattr(product, 'fashion'):
            serializer = FashionSerializer(product.fashion)
        else:
            serializer = ProductSerializer(product)
        return Response(serializer.data)
```

## product-service/urls.py

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```
