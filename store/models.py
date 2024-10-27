from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Ensure category names are unique

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')  # Link products to category
    image = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Upload an image of the product")  # Allows optional images

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"  # Show price in string representation


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')  # Each user has one cart

    def __str__(self):
        return f"{self.user.username}'s cart"

    def total_items(self):
        return self.cart_items.count()  # Count of items in the cart

    def total_price(self):
        total = sum(item.total_price() for item in self.cart_items.all())  # Calculate total price of all items
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')  # Associate cart items with a cart
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')  # Associate cart item with a product
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product
    added_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the product was added to the cart

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart.user.username}'s cart"

    def total_price(self):
        return self.quantity * self.product.price  # Calculate total price for this cart item


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, default='Not Provided')
    contact_number = models.CharField(max_length=15, blank=True,default='Not Porvided')
    
    def __str__(self):
        return self.user.username
    


class IntelProduct(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # Add other relevant fields for your product

    def __str__(self):
        return self.name