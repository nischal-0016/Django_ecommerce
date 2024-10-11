from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Product, Category, Cart,CartItem
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def product_list(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'store/product_list.html', {'products': products})

def category_list(request):
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'store/category_list.html', {'categories': categories})

def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)  # Fetch the specific product by its ID
    context = {
        'product': product,
    } 
    return render(request, 'store/product_detail.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to your desired page after login
        else:
            # Check if the username exists
            if not User.objects.filter(username=username).exists():
                messages.info(request, 'This username does not exist. Please register.')
            else:
                messages.error(request, 'Invalid username or password.')

    return render(request, 'store/login.html')

def add_to_cart(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You need to log in to add items to the cart.'}, status=403)

    product = get_object_or_404(Product, pk=pk)
    user = request.user

    # Get or create a Cart for the user
    cart, created = Cart.objects.get_or_create(user=user)

    # Get or create a CartItem for the cart and product
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1  # Increment quantity if already in cart
        cart_item.save()

    # Calculate the total items in cart
    cart_count = CartItem.objects.filter(cart=cart).count()  # Count the items in the cart

    return JsonResponse({'cart_count': cart_count})

@login_required
def cart_view(request):
    user = request.user
    cart = get_object_or_404(Cart, user=user)  # Fetch the user's cart
    cart_items = cart.cart_items.all()  # Fetch the cart items for the user's cart

    total_price = sum(item.total_price() for item in cart_items)  # Calculate total price

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'store/cart.html', context)
