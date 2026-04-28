from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Payment
from .serializers import PaymentSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=['post'])
    def pay(self, request):
        order_id = request.data.get('order_id')
        amount = request.data.get('amount')
        payment = Payment.objects.create(order_id=order_id, amount=amount)
        # Giả lập thanh toán thành công
        payment.status = 'SUCCESS'
        payment.save()
        return Response({'payment_id': payment.id, 'status': 'SUCCESS'})

    @action(detail=False, methods=['get'])
    def status(self, request):
        order_id = request.query_params.get('order_id')
        try:
            payment = Payment.objects.get(order_id=order_id)
            return Response({'status': payment.status})
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=404)