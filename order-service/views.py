from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        user_id = request.data.get('user_id')
        # Giả sử gọi cart-service để lấy items
        # Ở đây giả lập
        items = request.data.get('items', [])
        total_price = sum(item['price'] * item['quantity'] for item in items)

        order = Order.objects.create(user_id=user_id, total_price=total_price)
        for item in items:
            OrderItem.objects.create(
                order=order,
                product_id=item['product_id'],
                quantity=item['quantity']
            )
        # Gọi payment-service
        return Response({'order_id': order.id, 'status': 'CREATED'})