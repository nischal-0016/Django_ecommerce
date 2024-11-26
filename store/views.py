from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Product, Category, Cart, CartItem, IntelProduct, AMDProduct, IntelCategory, AMDCategory
from .forms import CustomUserCreationForm, UserForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# View to list all products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

# View to list all categories on homepage
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})

# View to show product details
def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'store/product_detail.html', {'product': product})

# User registration view
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

# User login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            if not User.objects.filter(username=username).exists():
                messages.info(request, 'This username does not exist. Please register.')
            else:
                messages.error(request, 'Invalid username or password.')

    return render(request, 'store/login.html')

# User profile view with form handling
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'store/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

# View for Intel PC build page
def intel_build(request):
    category_id = request.GET.get('category_id')
    categories = IntelCategory.objects.all()
    
    if category_id:
        products = IntelProduct.objects.filter(category_id=category_id)
    else:
        products = []

    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'store/intel_build.html', context)

# View for AMD PC build page
def amd_pc_build(request):
    category_id = request.GET.get('category_id')
    categories = AMDCategory.objects.all()
    
    if category_id:
        products = AMDProduct.objects.filter(category_id=category_id)
    else:
        products = []

    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'store/amd_build.html', context)

# Cart view to display cart items
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

# Add product to cart (general)
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({'success': True, 'message': 'Product added to cart'})

@login_required
def add_intel_product_to_cart(request, product_id):
    product = get_object_or_404(IntelProduct, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, intel_product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

# Add AMD product to cart
@login_required
def add_amd_product_to_cart(request, product_id):
    product = get_object_or_404(AMDProduct, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, amd_product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

    return JsonResponse({'success': True, 'message': 'AMD product added to cart'})


# Remove item from cart
@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        try:
            # Fetch and delete the cart item
            cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            cart_item.delete()

            # Calculate the total cart price after item removal
            total_cart_price = sum(item.total_price() for item in request.user.cart.cart_items.all())

            return JsonResponse({'success': True, 'total_cart_price': total_cart_price})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


    
# # Update cart quantity
# @login_required
# def update_cart_quantity(request, product_id):
#     if request.method == 'POST':
#         product = get_object_or_404(Product, id=product_id)
#         cart_item = get_object_or_404(CartItem, product=product, cart__user=request.user)
#         quantity = int(request.POST.get('quantity', 1))

#         if quantity < 1:
#             return JsonResponse({'error': 'Quantity must be at least 1.'}, status=400)

#         cart_item.quantity = quantity
#         cart_item.save()
#         item_total_price = cart_item.total_price()
#         total_cart_price = sum(item.total_price() for item in request.user.cart.cart_items.all())

#         return JsonResponse({
#             'item_total_price': item_total_price,
#             'total_cart_price': total_cart_price
#         })
#     return JsonResponse({'error': 'Invalid request'}, status=400)

def custom_pc_build(request):
    category_id = request.GET.get('category_id')
    pc_type = request.GET.get('pc_type')  # 'intel' or 'amd'
    
    categories = None
    products = []

    if pc_type == 'intel':
        categories = IntelCategory.objects.all()
        if category_id:
            products = IntelProduct.objects.filter(category_id=category_id)
    elif pc_type == 'amd':
        categories = AMDCategory.objects.all()
        if category_id:
            products = AMDProduct.objects.filter(category_id=category_id)
    
    context = {
        'categories': categories,
        'products': products,
        'pc_type': pc_type,
    }
    return render(request, 'store/custom_pc_build.html', context)
