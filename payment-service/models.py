from django.db import models

class Payment(models.Model):
    order_id = models.IntegerField()
    amount = models.FloatField()
    status = models.CharField(max_length=50, default='PENDING')

    def __str__(self):
        return f"Payment for order {self.order_id}"