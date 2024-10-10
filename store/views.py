from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Product, Category, Cart  
from .forms import CustomUserCreationForm

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
        messages.warning(request, 'You need to log in to add items to the cart.')
        return redirect('login')

    product = get_object_or_404(Product, pk=pk)
    user = request.user

    # Get or create a Cart item for the user and product
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)

    if not created:
        cart_item.quantity += 1  # Increment quantity if already in cart
        cart_item.save()

    messages.success(request, f'Added {product.name} to your cart.')
    return redirect('product_detail', pk=pk)  # Redirect back to product detail
