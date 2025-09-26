from django.urls import path
from shop import views
urlpatterns = [
    path('', views.base, name='base'),
    path('shop/category/<int:category_id>', views.categories, name='categories'),
    path('shop/all_products', views.all_products, name='all_products'),
    path('shop/add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('shop/remove_from_cart/<int:cart_item_id>', views.remove_from_cart, name='remove_from_cart'),
    path('shop/update_cart/<int:cart_item_id>', views.update_cart, name='update_cart'),
    path('cart', views.cart, name='cart'),
    path('shop/order_confirmation', views.order_confirmation, name='order_confirmation'),
]