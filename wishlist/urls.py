
from django.urls import path
from . import views
app_name='wishlist'
urlpatterns = [
  
    path('add_wishlist/<int:product_id>/',views.add_wishlist,name="add_wishlist"),
    path('wishlist/',views.wishlist,name="wishlist"),
    path('remove_wishlist_cart/<int:product_id>/<int:wishlist_item_id>/',views.remove_from_wishlist,name="remove_from_wishlist"),
    path('wishlist/add_to_cart/<int:product_id>',views.add_wishlist_item_to_cart, name="add_wishlist_to_cart"),

]