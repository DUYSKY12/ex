from django.db import models

class Cart(models.Model):
    user_id = models.IntegerField()

    def __str__(self):
        return f"Cart for user {self.user_id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    # Tham chiếu mềm: product_id là IntegerField thay vì ForeignKey tới product-service
    product_id = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    def __str__(self):
        return f"Item {self.product_id} in cart {self.cart.id}"