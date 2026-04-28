from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Shipment
from .serializers import ShipmentSerializer

class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

    @action(detail=False, methods=['post'])
    def create_shipment(self, request):
        order_id = request.data.get('order_id')
        address = request.data.get('address')
        shipment = Shipment.objects.create(order_id=order_id, address=address)
        return Response({'shipment_id': shipment.id, 'status': 'PROCESSING'})

    @action(detail=False, methods=['get'])
    def status(self, request):
        order_id = request.query_params.get('order_id')
        try:
            shipment = Shipment.objects.get(order_id=order_id)
            return Response({'status': shipment.status})
        except Shipment.DoesNotExist:
            return Response({'error': 'Shipment not found'}, status=404)