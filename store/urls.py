from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import payment_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Home and Product URLs
    path('', views.product_list, name='home'),  # Main page to list all products
    path('categories/', views.category_list, name='category_list'),  # Category listing page

    # Update URL pattern to accept string-based custom IDs for products
    path('product/<str:pk>/', views.product_detail, name='product_detail'),  # Product detail page for any product

    # Cart-related URLs for general products
    path('product/<str:product_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),  # General add to cart

    # Separate URLs for adding Intel and AMD products to the cart
    path('product/intel/<str:product_id>/add-to-cart/', views.add_intel_product_to_cart, name='add_intel_product_to_cart'),  # Intel product add
    path('product/amd/<str:product_id>/add-to-cart/', views.add_amd_product_to_cart, name='add_amd_product_to_cart'),  # AMD product add

    # Cart management URLs
    path('cart/', views.cart_view, name='cart'),  # Cart page

    # path('cart/update/<str:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),  # Update quantity in the cart
    path('cart/remove/<str:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove item from cart

    # User Authentication URLs
    path('login/', views.login_view, name='login'),  # Login page
    path('register/', views.register, name='register'),  # Registration page
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Logout functionality

    # User Profile page
    path('profile/', views.profile, name='profile'),  

    # Custom PC Build URLs
    path('custom-pc-build/', views.custom_pc_build, name='custom_pc_build'),  # Custom PC build main page
    path('custom-pc-build/intel/', views.intel_build, name='intel_build'),  # Intel-based custom PC build
    path('custom-pc-build/amd/', views.amd_pc_build, name='amd_build'),  # AMD-based custom PC build

    path('order/', views.order_page, name='order'),

    path('payment/', payment_view, name='payment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
