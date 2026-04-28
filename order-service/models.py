from django.db import models

class Order(models.Model):
    user_id = models.IntegerField()
    total_price = models.FloatField()
    status = models.CharField(max_length=50, default='CREATED')

    def __str__(self):
        return f"Order {self.id} for user {self.user_id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return f"Item {self.product_id} in order {self.order.id}"