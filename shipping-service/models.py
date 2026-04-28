from django.db import models

class Shipment(models.Model):
    order_id = models.IntegerField()
    address = models.TextField()
    status = models.CharField(max_length=50, default='PROCESSING')

    def __str__(self):
        return f"Shipment for order {self.order_id}"