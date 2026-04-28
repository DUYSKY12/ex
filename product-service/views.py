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