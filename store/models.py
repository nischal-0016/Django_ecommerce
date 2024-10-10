from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Ensure category names are unique
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Allows optional images

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"  # Show price in string representation

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate cart with a user
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Associate cart with a product
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product
    added_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the product was added to the cart

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.user.username}'s cart"
