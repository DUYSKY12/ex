from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=False, methods=['post'])
    def add(self, request):
        user_id = request.data.get('user_id')
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        cart, created = Cart.objects.get_or_create(user_id=user_id)
        item, item_created = CartItem.objects.get_or_create(
            cart=cart, product_id=product_id,
            defaults={'quantity': 0}
        )
        item.quantity += quantity
        item.save()
        return Response({'message': 'Added to cart'})

    @action(detail=False, methods=['delete'])
    def remove(self, request):
        user_id = request.data.get('user_id')
        product_id = request.data.get('product_id')

        try:
            cart = Cart.objects.get(user_id=user_id)
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.delete()
            return Response({'message': 'Removed from cart'})
        except Cart.DoesNotExist or CartItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=404)