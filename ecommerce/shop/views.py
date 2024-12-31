from django.shortcuts import render,redirect
from .models import Product, Cart, Order, CartItem

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not logged in
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')

def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        return render(request, 'shop/checkout.html', {'error': 'Your cart is empty!'})

    # Calculate total price for each item and overall total
    for item in cart_items:
        item.total_price = item.product.price * item.quantity  # Add total_price attribute to each cart item

    total_price = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        # Create an order
        order = Order.objects.create(user=request.user, total_price=total_price)
        # Clear the cart
        cart_items.delete()
        return render(request, 'shop/checkout.html', {'success': 'Order placed successfully!'})

    return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total_price': total_price})

def order_summary(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'shop/order_summary.html', {'cart_items': cart_items, 'total_price': total_price})