from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Product, Category, Cart,CartItem, IntelProduct, AMDProduct, IntelCategory, AMDCategory,Order, OrderItem
from .forms import CustomUserCreationForm, UserForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.conf import settings
import pdfkit,os
from django.views.decorators.http import require_POST
import requests
import uuid
from django.http import HttpResponseBadRequest
from django.urls import reverse


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

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()
        return JsonResponse({'success': True, 'message': 'Product added to cart'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})



# Remove item from cart
@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        try:
            cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            cart_item.delete()

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


@login_required
def order_page(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.cart_items.all()
    total_cost = sum(item.total_price() for item in items)

    return render(request, 'store/order.html', {'cart': cart, 'items': items, 'total_cost': total_cost})

def payment_view(request):
    return render(request, 'store/payment.html')

# invoice generation view
@login_required
def cash_on_delivery(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)

    total_price = sum(item.total_price() for item in cart_items)

    order = Order.objects.create(
        user=request.user,
        total_price=total_price,
        payment_method="Cash on Delivery",
        status="Pending"
    )

    # Generate invoice HTML
    invoice_html = render_to_string('store/invoice_template.html', {'order': order, 'cart_items': cart_items})

    pdf_file_name = f"invoice_{order.id}.pdf"
    pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'invoices', pdf_file_name)

    os.makedirs(os.path.dirname(pdf_file_path), exist_ok=True)

    # Generate PDF
    pdfkit.from_string(invoice_html, pdf_file_path, configuration=settings.PDFKIT_CONFIG)

    order.invoice.name = f"invoices/{pdf_file_name}"
    order.save()

    pdf_url = f"{settings.MEDIA_URL}invoices/{pdf_file_name}"

    return render(request, 'store/cashondelivery.html', {'pdf_url': pdf_url})

def intel_build(request):
    categories = IntelCategory.objects.prefetch_related('intel_products').all()
    products = IntelProduct.objects.all() 

    context = {
        'categories': categories,
    }
    return render(request, 'store/intel_build.html', context)


@login_required
def add_intel_product_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(IntelProduct, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, intel_product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse({"success": True, "redirect_url": '/cart/'})
    
    return JsonResponse({"error": "Invalid request"}, status=400)



def get_intel_products_by_category(request, category_id):
    products = IntelProduct.objects.filter(category_id=category_id)
    data = []

    for product in products:
        data.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'image_url': product.image.url if product.image else '',
        })

    return JsonResponse({'products': data})


@require_POST
@login_required
def add_selected_intel_products_to_cart(request):
    product_ids = request.POST.getlist('product_ids[]')
    
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    for product_id in product_ids:
        product = get_object_or_404(IntelProduct, id=product_id)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, intel_product=product)
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    
    return JsonResponse({'success': True, 'message': 'Products added to cart successfully.', 'redirect_url': '/cart/'})

def amd_build(request):
    categories = AMDCategory.objects.prefetch_related('amd_products').all()
    products = AMDProduct.objects.all()

    context = {
        'categories': categories,
    }
    return render(request, 'store/amd_build.html', context)

@login_required
def add_amd_product_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(AMDProduct, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, amd_product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse({"success": True, "redirect_url": '/cart/'})
    
    return JsonResponse({"error": "Invalid request"}, status=400)

def get_amd_products_by_category(request, category_id):
    products = AMDProduct.objects.filter(category_id=category_id)
    data = []

    for product in products:
        data.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'image_url': product.image.url if product.image else '',
        })

    return JsonResponse({'products': data})

@require_POST
@login_required
def add_selected_amd_products_to_cart(request):
    product_ids = request.POST.getlist('product_ids[]')
    
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    for product_id in product_ids:
        product = get_object_or_404(AMDProduct, id=product_id)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, amd_product=product)
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()

    return JsonResponse({'success': True, 'message': 'Products added to cart successfully.', 'redirect_url': '/cart/'})




@login_required
def initiate_khalti_cart_payment(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cart_items.all()
        cart_total = cart.total_price()

        if not cart_items:
            messages.error(request, "Your cart is empty. Add items to proceed with payment.")
            return redirect('cart')

        amount = float(cart_total)
        name = request.user.get_full_name() or request.user.username
        email = request.user.email
        phone = request.user.profile.contact_number or ""

        amount_in_paisa = int(amount * 100)

        order_id = str(uuid.uuid4())

        order = Order.objects.create(
            user=request.user,
            address=request.user.profile.address or "Not Provided",
            total_price=amount,
            payment_method="Khalti",
            status="Pending",
            khalti_token=order_id 
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                intel_product=item.intel_product,
                amd_product=item.amd_product,
                quantity=item.quantity,
                price=item.get_price()
            )

        customer_info = {
            "name": name,
            "email": email,
        }
        if phone and phone.strip():
            customer_info["phone"] = phone

        payload = {
            "return_url": settings.WEBSITE_URL + reverse('verify_khalti_cart_payment'),
            "website_url": settings.WEBSITE_URL,
            "amount": amount_in_paisa,
            "purchase_order_id": order_id,
            "purchase_order_name": f"Cart Order {order.id}",
            "customer_info": customer_info
        }

        headers = {
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                f"{settings.KHALTI_API_URL}epayment/initiate/",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()

            if 'payment_url' in data:
                return redirect(data['payment_url'])
            else:
                messages.error(request, "Failed to initiate payment. Please try again.")
                order.delete()
                return redirect('cart')

        except requests.RequestException as e:
            messages.error(request, f"Payment initiation failed: {str(e)}")
            order.delete()
            return redirect('cart')

    return HttpResponseBadRequest("Invalid request method.")

@login_required
def verify_khalti_cart_payment(request):
    pidx = request.GET.get('pidx')
    status = request.GET.get('status')
    transaction_id = request.GET.get('transaction_id')
    purchase_order_id = request.GET.get('purchase_order_id')

    if not pidx:
        messages.error(request, "Invalid payment verification request.")
        return redirect('cart')

    lookup_url = f"{settings.KHALTI_API_URL}epayment/lookup/"
    headers = {
        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"pidx": pidx}

    try:
        response = requests.post(lookup_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        try:
            order = Order.objects.get(khalti_token=purchase_order_id) 
        except Order.DoesNotExist:
            messages.error(request, "Invalid transaction.")
            return redirect('cart')

        if data.get('status') == 'Completed':
            order.status = "Completed"
            order.save()

            # Clear the cart after successful payment
            Cart.objects.get(user=request.user).cart_items.all().delete()

            messages.success(
                request,
                "Payment successful! Your order has been placed."
            )
            return redirect('cart')
        else:
            status = data.get('status')
            if status in ['Expired', 'User canceled']:
                messages.error(request, f"Payment {status.lower()}. Please try again.")
                order.delete()
            elif status == 'Pending':
                messages.warning(request, "Payment is pending. Please contact support if not resolved soon.")
            elif status == 'Refunded':
                messages.error(request, "Payment was refunded. Please contact support.")
            else:
                messages.error(request, "Payment failed. Please try again.")
                order.delete()

            return redirect('cart')

    except requests.RequestException as e:
        messages.error(request, f"Payment verification failed: {str(e)}")
        return redirect('cart')

@login_required
def payment_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_total = cart.total_price()
    except Cart.DoesNotExist:
        cart_total = 0
    return render(request, 'store/payment.html', {'cart_total': cart_total})


@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # Verify the old password
        user = authenticate(username=request.user.username, password=old_password)
        if user is None:
            messages.error(request, 'Old password is incorrect.')
            return render(request, 'store/password_change.html')

        # Check if new passwords match
        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return render(request, 'store/password_change.html')

        if len(new_password1) < 8:
            messages.error(request, 'New password must be at least 8 characters long.')
            return render(request, 'store/password_change.html')

        request.user.set_password(new_password1)
        request.user.save()

        update_session_auth_hash(request, request.user)

        messages.success(request, 'Your password was successfully updated!')
        return redirect('profile')

    return render(request, 'store/password_change.html')