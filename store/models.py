from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=100)  
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Upload an image of the product")

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"

# Separate category model for INTEL products
class IntelCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# AMD-specific product model linked to INETLCategory
class IntelProduct(models.Model):
    id = models.CharField(primary_key=True, max_length=100) 
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # description = models.TextField(blank=True, null=True)
    category = models.ForeignKey('IntelCategory', on_delete=models.CASCADE, related_name='intel_products')
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
    id = models.CharField(primary_key=True, max_length=100) 
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # description = models.TextField(blank=True, null=True)
    category = models.ForeignKey('AMDCategory', on_delete=models.CASCADE, related_name='amd_products')
    image = models.ImageField(upload_to='amd_products/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"
    

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"{self.user.username}'s cart"

    def total_items(self):
        return self.cart_items.count()

    def total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items', null=True, blank=True)
    intel_product = models.ForeignKey(IntelProduct, on_delete=models.CASCADE, related_name='cart_items', null=True, blank=True)
    amd_product = models.ForeignKey(AMDProduct, on_delete=models.CASCADE, related_name='cart_items', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.product:
            return f"{self.quantity} of {self.product.name} in {self.cart.user.username}'s cart"
        elif self.intel_product:
            return f"{self.quantity} of {self.intel_product.name} in {self.cart.user.username}'s cart"
        elif self.amd_product:
            return f"{self.quantity} of {self.amd_product.name} in {self.cart.user.username}'s cart"

    def total_price(self):
        if self.product:
            return self.quantity * self.product.price
        elif self.intel_product:
            return self.quantity * self.intel_product.price
        elif self.amd_product:
            return self.quantity * self.amd_product.price


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, default='Not Provided')
    contact_number = models.CharField(max_length=15, blank=True, default='Not Provided')

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, default='Not Provided')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default="Pending") 
    created_at = models.DateTimeField(auto_now_add=True)
    invoice = models.FileField(upload_to='invoices/', blank=True, null=True)

