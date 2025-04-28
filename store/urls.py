from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import payment_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Home and Product URLs
    path('', views.product_list, name='home'),  
    path('categories/', views.category_list, name='category_list'),  

    # Update URL pattern to accept string-based custom IDs for products
    path('product/<str:pk>/', views.product_detail, name='product_detail'),  

    # Cart-related URLs for general products
    path('product/<str:product_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),  

    # Separate URLs for adding Intel and AMD products to the cart
    path('product/intel/<str:product_id>/add-to-cart/', views.add_intel_product_to_cart, name='add_intel_product_to_cart'), 
    path('product/amd/<str:product_id>/add-to-cart/', views.add_amd_product_to_cart, name='add_amd_product_to_cart'),  

    # Cart management URLs
    path('cart/', views.cart_view, name='cart'),  # Cart page
    path('cart/remove/<str:item_id>/', views.remove_from_cart, name='remove_from_cart'),  

    # User Authentication URLs
    path('login/', views.login_view, name='login'),  
    path('register/', views.register, name='register'),  
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  

    # User Profile page
    path('profile/', views.profile, name='profile'),  
    path('profile/', views.profile, name='profile'),  
    path('password_change/', views.change_password, name='password_change'),

    # Custom PC Build URLs
    path('custom-pc-build/', views.custom_pc_build, name='custom_pc_build'),  
    path('custom-pc-build/intel/', views.intel_build, name='intel_build'),
    path('custom-pc-build/intel/product/<int:product_id>/add-to-cart/', views.add_intel_product_to_cart, name='add_intel_product_to_cart'),
    path('custom-pc-build/intel/add-to-cart/', views.add_selected_intel_products_to_cart, name='add_selected_intel_products_to_cart'),


    # AMD build
    path('custom-pc-build/amd/', views.amd_build, name='amd_build'),
    path('custom-pc-build/amd/product/<str:product_id>/add-to-cart/', views.add_amd_product_to_cart, name='add_amd_product_to_cart'),
    path('custom-pc-build/amd/add-to-cart/', views.add_selected_amd_products_to_cart, name='add_selected_amd_products_to_cart'),

    # Order & Payment
    path('order/', views.order_page, name='order'),
    path('payment/', payment_view, name='payment'),
    path('cash_on_delivery/', views.cash_on_delivery, name='cash_on_delivery'),
    path('initiate-khalti-cart-payment/', views.initiate_khalti_cart_payment, name='initiate_khalti_cart_payment'),
    path('verify-khalti-cart-payment/', views.verify_khalti_cart_payment, name='verify_khalti_cart_payment'),
    path('payment/', views.payment_view, name='payment'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)