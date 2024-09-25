
from django.http import HttpResponse
from django.shortcuts import render
from store.models import Product
import random

def featured(request):
  
    products = Product.objects.all()

   
    product_count = products.count()
    if product_count < 7:
        rand_prod = products  
    else:
        listed = list(products)  # Convert queryset to a list
        rand_prod = random.sample(listed, k=7)  # Randomly sample 3 products

    print(rand_prod)

    context = {
        'rand_prod': rand_prod,
        'active_tab': 'featured'
    }
    return render(request, 'home.html', context)

def sales(request):

    sales = Product.objects.filter(sale=True)
    print(sales)
    print("Sales products:", sales)

    return render(request, 'home.html', {'sales': sales, 'active_tab': 'sales'})

def  rated(request):

    rated = Product.objects.filter(top_rated=True)
    print(rated)
    print("rated products:", rated)

    return render(request, 'home.html', {'rated': rated, 'active_tab': 'rated'})