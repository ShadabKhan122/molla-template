from .models import Wishlist,WishlistItem
from .views import _wishlist_id

def counter(request):
    wishlist_count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            if request.user.is_authenticated:
                wishlist_items=WishlistItem.objects.filter(user=request.user)
            else:

                wishlist=Wishlist.objects.filter(wishlist_id=_wishlist_id(request))
                wishlist_items=WishlistItem.objects.filter(wishlist=wishlist[:1])
            for wishlist_item in wishlist_items:
                wishlist_count+=wishlist_item.quantity
        except Wishlist.DoesNotExist:
            wishlist_count=0
    return dict(wishlist_count=wishlist_count)