from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.product_list, name='home'),  # Home page shows all products

    path('categories/', views.category_list, name='category_list'),  # Category list

    path('product/<int:pk>/', views.product_detail, name='product_detail'),  # Product details

    path('product/<int:pk>/add-to-cart/', views.add_to_cart, name='add_to_cart'),  # Add to Cart functionality

    path('login/', views.login_view, name='login'),  # Custom login view

    path('register/', views.register, name='register'),  # Registration view

    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Logout view
    
    path('cart/', views.cart_view, name='cart'),  # Cart view URL

    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
