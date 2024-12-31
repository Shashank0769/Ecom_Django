from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/',views.checkout_view,name='checkout_view'),
    path('order_summary/',views.order_summary,name='order_summary'),
]
