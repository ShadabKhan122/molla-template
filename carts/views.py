from django.shortcuts import render,redirect
from store.models import Product,Variation
from .models import Cart,CartItem
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal

# Create your views here.
def _cart_id(request):
    cart=request.session.session_key#ye session id jo created hai wo fetch karega
    if not cart:
        cart=request.session.create()#ye code session id create karega
    return cart

def add_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    rental_days = 0
    if request.user.is_authenticated:

        product_variation=[]
      
        if request.method == "POST":
            rental_days = request.POST.get('rental_days', '0')
            rental_days = int(rental_days) 
            for item in request.POST:
                key=item
                
                value=request.POST[key]
               

                try:
                    variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    
                    product_variation.append(variation)
                except:
                    pass

                
        
        is_cart_item_exists=CartItem.objects.filter(product=product,user=request.user).exists()
        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(product=product,user=request.user)
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item=CartItem.objects.get(product=product,id=item_id)
                
                item.quantity+=1
                item.rental_days = rental_days
                item.save()
            else:
                item=CartItem.objects.create(product=product,quantity=1,user=request.user)
                if len(product_variation)>0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()
                    
        else:
            cart_item=CartItem.objects.create(
                product=product,
                quantity=1,
                user=request.user,
                rental_days=rental_days 
            )
            if len(product_variation)>0:
                    cart_item.variation.clear()
                    cart_item.variation.add(*product_variation)
                
            cart_item.save()
    else:
        product_variation=[]
   

        if request.method == "POST":
            for item in request.POST:
                key=item
                print(f'Key is:{key}')
                value=request.POST[key]
                print(value)
                try:
                    variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    print(variation)
                    product_variation.append(variation)
                except:
                    pass

                print(f'Your variation is:{product_variation}')
                

        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart=Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()
        
        is_cart_item_exists=CartItem.objects.filter(product=product,cart=cart).exists()
        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(product=product,cart=cart)
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            if product_variation in ex_var_list:
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item=CartItem.objects.get(product=product,id=item_id)
                # print(item)
                item.quantity+=1
                item.save()
            else:
                item=CartItem.objects.create(product=product,quantity=1,cart=cart)
                if len(product_variation)>0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()
                    



        else:
            cart_item=CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )
            if len(product_variation)>0:
                    cart_item.variation.clear()
                    cart_item.variation.add(*product_variation)
                
            cart_item.save()
    return redirect('carts:cart')

def cart(request):
    tax=Decimal(0)
    total=Decimal(0)
    final_total=Decimal(0)
    total_rent = Decimal(0)
    if request.user.is_authenticated:
        
        cart_items=CartItem.objects.filter(user=request.user,is_active=True)
    else:
        return redirect ('home')
        # cart=Cart.objects.get(cart_id=_cart_id(request))
        # cart_items=CartItem.objects.filter(cart=cart,is_active=True)
    
    for cart_item in cart_items:
        total+=cart_item.product.price*cart_item.quantity
        total_rent += cart_item.rent_total() 
        tax=(total*8)/100
        final_total=total+tax+total_rent
    context={
        'cart_items':cart_items,
        'total':total,
        'tax':tax,
        'final_total':final_total,
        'total_rent': total_rent,
    }


    return render(request,'cart.html',context)



def remove_cart(request,product_id,cart_item_id):
    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(user=request.user,product=product_id,id=cart_item_id)
    else:

        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItem.objects.get(cart=cart,product=product_id,id=cart_item_id)
    cart_item.delete()
    return redirect('carts:cart')

def remove_item(request,product_id,cart_item_id):
    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(user=request.user,product=product_id,id=cart_item_id)
    else:

        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItem.objects.get(cart=cart,product=product_id,id=cart_item_id)
    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
        return redirect('carts:cart')
    else:
        cart_item.quantity = 1
        cart_item.save()
        messages.info(request, "Item quantity cannot be less than 1.")
        return redirect('carts:cart')

@login_required(login_url="accounts:login")
def checkout(request,total=0,quantity=0,total_rent=0,cart_items=None):
    try:
        tax=0
        final_total=0
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total=total+(cart_item.product.price*cart_item.quantity) 
            quantity=quantity+cart_item.quantity
        tax=(8*total)/100
        final_total=total+tax+total_rent
    except Exception:
        pass
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'final_total':final_total,
    }

    return render(request,'store/checkout.html',context)

from django.shortcuts import redirect, get_object_or_404


def update_rental_days(request, product_id, cart_item_id):
    if request.method == "POST":
        rental_days = request.POST.get('rental_days', '0')
        rental_days = int(rental_days)  # Convert to integer

        if request.user.is_authenticated:
            cart_item = get_object_or_404(CartItem, user=request.user, product=product_id, id=cart_item_id)
        else:
            cart = get_object_or_404(Cart, cart_id=_cart_id(request))
            cart_item = get_object_or_404(CartItem, cart=cart, product=product_id, id=cart_item_id)

        cart_item.rental_days = rental_days
        cart_item.save()

    return redirect('carts:cart')

def rent_product(request, product_id):
    if request.method == "POST":
        rental_days = request.POST.get('rental_days', '0')
        rental_days = int(rental_days)
        
        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            product_variation = []
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except Variation.DoesNotExist:
                    pass

            cart_item, created = CartItem.objects.get_or_create(
                product=product,
                user=request.user,
                defaults={'quantity': 1, 'rental_days': rental_days}
            )

            if not created:
                cart_item.rental_days = rental_days
                cart_item.save()

            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
                cart_item.save()

        return redirect('carts:cart')
