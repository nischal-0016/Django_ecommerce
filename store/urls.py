from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.product_list, name='home'),  # Home page shows all products
    path('categories/', views.category_list, name='category_list'),  # Category list
    path('product/<int:pk>/', views.product_detail, name='product_detail'),  # Product details
    # Use the built-in LoginView or your custom login_view
    path('login/', views.login_view, name='login'),  # Custom login view
    path('register/', views.register, name='register'),  # Registration view
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Logout view
]
