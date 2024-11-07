from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Main Category model for homepage
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# Product model linked to the main Category model for homepage products
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Upload an image of the product")

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"

# Separate category model for Intel products
class IntelCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# Intel-specific product model linked to IntelCategory
class IntelProduct(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(IntelCategory, on_delete=models.CASCADE, related_name='intel_products')
    image = models.ImageField(upload_to='intel_products/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"

# Separate category model for AMD products
class AMDCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# AMD-specific product model linked to AMDCategory
class AMDProduct(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(AMDCategory, on_delete=models.CASCADE, related_name='amd_products')
    image = models.ImageField(upload_to='amd_products/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"

# Cart model for users
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"{self.user.username}'s cart"

    def total_items(self):
        return self.cart_items.count()

    def total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())

# Cart item model for adding products to the cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart.user.username}'s cart"

    def total_price(self):
        return self.quantity * self.product.price

# Profile model for user information
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, default='Not Provided')
    contact_number = models.CharField(max_length=15, blank=True, default='Not Provided')

    def __str__(self):
        return self.user.username
