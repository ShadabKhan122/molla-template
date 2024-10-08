from django.shortcuts import render,redirect
from store.models import Product,Variation
from .models import WishlistItem,Wishlist
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from carts.models import CartItem
from category.models import Category

# Create your views here.
def _wishlist_id(request):
    # Get the current session key
    wishlist = request.session.get('wishlist_id', None)

    # If there is no wishlist ID, create a new session key
    if not wishlist:
        # Create a new session if it doesn't exist
        if not request.session.session_key:
            request.session.create()
        # Assign a unique wishlist ID
        wishlist = request.session.session_key  # or you could use a UUID as shown earlier
        request.session['wishlist_id'] = wishlist  # Store the wishlist ID in the session

    return wishlist

def add_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        product_variation = []

        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]


                if key == 'quantity':
                    quantity = int(value)
                else:
                    quantity = 1

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

                

        # Check if the wishlist item already exists for the user
        is_wishlist_item_exists = WishlistItem.objects.filter(product=product, user=request.user).exists()

        if is_wishlist_item_exists:
            wishlist_items = WishlistItem.objects.filter(product=product, user=request.user)
            ex_var_list = []
            id = []

            for item in wishlist_items:
                existing_variations = item.variation.all()
                ex_var_list.append(list(existing_variations))
                id.append(item.id)

            if product_variation in ex_var_list:
                # If the product with the same variation exists, do nothing (don't add a duplicate)
                pass
            else:
                # Update the existing wishlist item with new variation if needed
                wishlist_item = WishlistItem.objects.create(product=product, user=request.user)
                if product_variation:
                    wishlist_item.variation.clear()
                    wishlist_item.variation.add(*product_variation)
                wishlist_item.save()

        else:
            # Create a new wishlist item if it doesn't exist
            wishlist_item = WishlistItem.objects.create(
                product=product,
                user=request.user
            )
            if product_variation:
                wishlist_item.variation.clear()
                wishlist_item.variation.add(*product_variation)
            wishlist_item.save()

    else:
        product_variation = []

        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        try:
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        except Wishlist.DoesNotExist:
            wishlist = Wishlist.objects.create(
                wishlist_id=_wishlist_id(request)
            )
        wishlist.save()

        # Check if the wishlist item already exists in the wishlist (for guest users)
        is_wishlist_item_exists = WishlistItem.objects.filter(product=product, wishlist=wishlist).exists()

        if is_wishlist_item_exists:
            wishlist_items = WishlistItem.objects.filter(product=product, wishlist=wishlist)
            ex_var_list = []
            id = []

            for item in wishlist_items:
                existing_variations = item.variation.all()
                ex_var_list.append(list(existing_variations))
                id.append(item.id)

            if product_variation in ex_var_list:
                # If the product with the same variation exists, do nothing
                pass
            else:
                # Create a new wishlist item with different variations
                wishlist_item = WishlistItem.objects.create(product=product, wishlist=wishlist)
                if product_variation:
                    wishlist_item.variation.clear()
                    wishlist_item.variation.add(*product_variation)
                wishlist_item.save()

        else:
            # Create a new wishlist item if it doesn't exist
            wishlist_item = WishlistItem.objects.create(
                product=product,
                wishlist=wishlist,
                quantity=quantity
            )
            if product_variation:
                wishlist_item.variation.clear()
                wishlist_item.variation.add(*product_variation)
            wishlist_item.save()

    return redirect('wishlist:wishlist')


def remove_from_wishlist(request,product_id,wishlist_item_id):
    if request.user.is_authenticated:
        wishlist_item=WishlistItem.objects.get(user=request.user,product=product_id, id=wishlist_item_id)
    else:

        return redirect('accounts:login')
    wishlist_item.delete()
    return redirect('wishlist:wishlist')

from django.shortcuts import render
from .models import Wishlist, WishlistItem

def wishlist(request,product_slug=None):
    
    
    if request.user.is_authenticated:
        # Get wishlist items for the authenticated user
        wishlist_items = WishlistItem.objects.filter(user=request.user)
    else:
        # Handle guest users by using session-based wishlist
        try:
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
            wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
        except Wishlist.DoesNotExist:
            wishlist_items = []
    
    in_stock_status = []
    for item in wishlist_items:
        in_stock_status.append(item.is_in_stock()) 

    context = {
        'wishlist_items': wishlist_items,
        'in_stock': in_stock_status
    }

    return render(request, 'store/wishlist.html', context)

def add_wishlist_item_to_cart(request,product_id):
    product=Product.objects.get( id=product_id)
    wishlist_items=WishlistItem.objects.filter(user=request.user,product=product).first()

    if wishlist_items:
        is_cart_item_exists = CartItem.objects.filter(user=request.user, product=product).exists()

        if is_cart_item_exists:
            cart_item=CartItem.objects.get(product=product,user=request.user)
            cart_item.quantity += 1
            cart_item.save()
        else:
            CartItem.objects.create(product=product ,quantity=1,user=request.user)
    

        wishlist_items.delete()
    
    return redirect('carts:cart')