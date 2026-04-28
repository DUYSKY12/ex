from django.db import models

class Laptop(models.Model):
    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    cpu = models.CharField(max_length=100)
    ram = models.CharField(max_length=50)
    gpu = models.CharField(max_length=100)
    storage = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.name}"
