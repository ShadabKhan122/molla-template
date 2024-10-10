from django.urls import path
from molla.views import sales,featured,rated,add_featured_item_to_cart,add_sales_item_to_cart,add_rated_item_to_cart
from .views import home
urlpatterns = [
    path('', home, name='home'),
    
    path('home/', featured, name='featured'),
    path('sale/', sales, name='sales'),
    path('rated/', rated, name='rated'),
    path('featured/add_to_cart/<int:product_id>',add_featured_item_to_cart,name='add_to_cart_featured'),
    path('sales/add_to_cart/<int:product_id>',add_sales_item_to_cart,name='add_to_cart_sales'),
    path('top_reated/add_to_cart/<int:product_id>',add_rated_item_to_cart,name='add_to_cart_rated'),
]
