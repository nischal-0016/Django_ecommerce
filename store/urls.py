from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Home and Product URLs
    path('', views.product_list, name='home'),  # Home page shows all products
    
    path('categories/', views.category_list, name='category_list'),  # Category list

    path('product/<int:pk>/', views.product_detail, name='product_detail'),  # Product details

    path('product/<int:product_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),  # Add to Cart functionality

    # User Authentication URLs
    path('login/', views.login_view, name='login'),  # Custom login view

    path('register/', views.register, name='register'),  # Registration view

    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Logout view

    # Cart-related URLs
    path('cart/', views.cart_view, name='cart'),  # View cart

    path('cart/update/<int:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),  # Update cart quantity

    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove item from cart

    path('profile/', views.profile, name='profile'),

    path('custom-pc-build/', views.custom_pc_build, name='custom_pc_build'),

    path('custom-pc-build/intel/', views.intel_build, name='intel_build'),  # Intel build URL
    
    path('custom-pc-build/amd/', views.amd_build, name='amd_build'),        # AMD build URL

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
