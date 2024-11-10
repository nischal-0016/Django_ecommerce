from django.contrib import admin
from .models import Category, Product, Profile, IntelCategory, IntelProduct, AMDCategory, AMDProduct

# Admin class for IntelProduct
class IntelProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'image')  # Display fields in the list view
    search_fields = ('name',)  # Allow searching by name
    list_filter = ('category',)  # Add filtering by category

# Admin class for AMDProduct
class AMDProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'image')  # Display fields in the list view
    search_fields = ('name',)  # Allow searching by name
    list_filter = ('category',)  # Add filtering by category

# Admin class for Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Admin class for IntelCategory
class IntelCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Admin class for AMDCategory
class AMDCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(IntelCategory, IntelCategoryAdmin)
admin.site.register(IntelProduct, IntelProductAdmin)
admin.site.register(AMDCategory, AMDCategoryAdmin)
admin.site.register(AMDProduct, AMDProductAdmin)
