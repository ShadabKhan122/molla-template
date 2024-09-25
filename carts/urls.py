from django.urls import path
from . import views
app_name='carts'
urlpatterns = [
  
    path('add_cart/<int:product_id>/',views.add_cart,name="add_cart"),
    path('cart/',views.cart,name="cart"),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.remove_cart,name="remove_cart"),
    path('remove_item/<int:product_id>/<int:cart_item_id>/',views.remove_item,name="remove_item"),
    path('checkout/',views.checkout,name="checkout"),
    path('update_rental_days/<int:product_id>/<int:cart_item_id>/', views.update_rental_days, name='update_rental_days'),
    path('rent/<int:product_id>/', views.rent_product, name='rent_product'),
]