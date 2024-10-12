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
        # Redirect to login if not authenticated
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    # Get the product by its primary key
    product = get_object_or_404(Product, pk=pk)

    # Get or create a cart for the logged-in user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get or create a cart item for the product
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        # If the cart item already exists, increment the quantity
        cart_item.quantity += 1
        cart_item.save()

    # Respond with JSON to update the cart count
    return JsonResponse({
        'cart_count': cart.total_items(),
        'message': 'Item added to cart successfully'
    })

def cart_view(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Try to get the cart for the logged-in user, or create one if it doesn't exist
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Get all cart items for the current user's cart
        cart_items = cart.cart_items.all()

        # Calculate the total price of items in the cart
        total_price = sum(item.total_price() for item in cart_items)

        # Pass cart items and total price to the template
        return render(request, 'store/cart.html', {  # Ensure the correct path to cart.html
            'cart_items': cart_items,
            'total_price': total_price,
            'cart_count': cart.total_items(),  # Ensure total_items() is correctly defined in your Cart model
        })
    else:
        # Redirect to login if the user is not authenticated
        return redirect('login')
    
def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        # Get the cart item by ID and delete it
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()

    # Redirect back to the cart page
    return redirect('cart')


