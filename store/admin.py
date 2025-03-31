from django.contrib import admin
from .models import Category, Product, Profile, IntelCategory, IntelProduct, AMDCategory, AMDProduct,Order

# Admin class for IntelProduct
class IntelProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'image')  
    search_fields = ('name',)  
    list_filter = ('category',) 

# Admin class for AMDProduct
class AMDProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'image') 
    search_fields = ('name',)  
    list_filter = ('category',)  

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
admin.site.register(Order)

admin.site.site_header = "PCGeek Admin Panel"
admin.site.site_title = "PCGeek Admin"
admin.site.index_title = "Welcome to PCGeek Administration"
