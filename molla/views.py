
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
import random
from carts.models import Cart,CartItem

def featured(request):
  
    products = Product.objects.all()

   
    product_count = products.count()
    if product_count < 7:
        rand_prod = products  
    else:
        listed = list(products)  # Convert queryset to a list
        rand_prod = random.sample(listed, k=7)  # Randomly sample 3 products

    

    context = {
        'rand_prod': rand_prod,
        'active_tab': 'featured'
    }
    return render(request, 'home.html', context)

def add_featured_item_to_cart(request, product_id):
    product=Product.objects.get( id=product_id)

    if product:
        is_cart_item_exists = CartItem.objects.filter(user=request.user, product=product).exists()

        if is_cart_item_exists:
            cart_item=CartItem.objects.get(product=product,user=request.user)
            cart_item.quantity += 1
            cart_item.save()
        else:
            CartItem.objects.create(product=product ,quantity=1,user=request.user)

    
    return redirect('carts:cart')


def sales(request):

    sales = Product.objects.filter(sale=True)
    print(sales)
    print("Sales products:", sales)

    return render(request, 'home.html', {'sales': sales, 'active_tab': 'sales'})

def add_sales_item_to_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    sale_product=Product.objects.filter(sale=True)
    if sale_product:
        is_cart_item_exits=CartItem.objects.filter(user=request.user, product=product).exists()

        if is_cart_item_exits:
            cart_item=CartItem.objects.get(product=product, user=request.user)
            cart_item.quantity +=1
            cart_item.save()
        else:
            CartItem.objects.create(product=product,quantity=1,user=request.user)
    
    return redirect('carts:cart')

def  rated(request):

    rated = Product.objects.filter(top_rated=True)
    print(rated)
    print("rated products:", rated)

    return render(request, 'home.html', {'rated': rated, 'active_tab': 'rated'})


def add_rated_item_to_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    rated_product=Product.objects.filter(top_rated=True).first()
    if rated_product:
        is_cart_item_exists=CartItem.objects.filter(user=request.user, product=product).exists()

        if is_cart_item_exists:
            cart_item=CartItem.objects.get(product=product,user=request.user)
            cart_item.quantity += 1
            cart_item.save()
        else:
            CartItem.objects.create(product=product,quantity =1, user=request.user)
        
    return redirect('carts:cart')
