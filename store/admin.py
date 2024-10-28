from django.contrib import admin
from .models import Category, Product, Profile, IntelProduct,AMDProduct

# Custom Admin class for IntelProduct
class IntelProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'image')  # Display fields in the list view
    search_fields = ('name',)  # Allow searching by name
    list_filter = ('category',)  # Add filtering by category

# Register models with the admin site
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(IntelProduct, IntelProductAdmin)
admin.site.register(AMDProduct)