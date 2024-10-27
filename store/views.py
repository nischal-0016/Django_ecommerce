from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Product, Category, Cart, CartItem, Profile,IntelProduct
from .forms import CustomUserCreationForm, UserForm, ProfileForm
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
    return render(request, 'store/product_detail.html', {'product': product})

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
            if not User.objects.filter(username=username).exists():
                messages.info(request, 'This username does not exist. Please register.')
            else:
                messages.error(request, 'Invalid username or password.')

    return render(request, 'store/login.html')

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        cart, _ = Cart.objects.get_or_create(user=request.user)  # Get or create cart for the user
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

        cart_count = cart.cart_items.count()

        return JsonResponse({'cart_count': cart_count})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.all()
    total_price = sum(item.total_price() for item in cart_items)

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart.total_items(),
    })

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()  # Delete the cart item

        # Calculate the updated total price for the cart
        total_cart_price = sum(item.total_price() for item in request.user.cart.cart_items.all())

        return JsonResponse({'total_cart_price': total_cart_price})  # Return updated total price
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def update_cart_quantity(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart_item = get_object_or_404(CartItem, product=product, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))

        # Ensure the quantity is at least 1
        if quantity < 1:
            return JsonResponse({'error': 'Quantity must be at least 1.'}, status=400)

        cart_item.quantity = quantity
        cart_item.save()

        item_total_price = cart_item.total_price()
        total_cart_price = sum(item.total_price() for item in request.user.cart.cart_items.all())

        return JsonResponse({
            'item_total_price': item_total_price,
            'total_cart_price': total_cart_price
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def profile(request):
    if request.method == 'POST':
        # Handle the user form and profile form
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)  # Assuming Profile is related to User

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            # Show success message
            return redirect('profile')  # Reload the page to clear POST data and show updated data
    else:
        # Prepopulate forms with current user data
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'store/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

def custom_pc_build(request):
    return render(request, 'store/custom_pc_build.html')

def intel_build(request):
    return render(request, 'intel_build.html')  # Placeholder view for Intel

def amd_build(request):
    return render(request, 'amd_build.html')    # Placeholder view for AMD

def intel_build(request):
    categories = Category.objects.all()  
    if 'category_id' in request.GET:
        category_id = request.GET['category_id']
        products = IntelProduct.objects.filter(category_id=category_id)
    else:
        products = IntelProduct.objects.all()
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'store/intel_build.html', context)