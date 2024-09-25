from django.shortcuts import render,redirect,get_object_or_404
from category.models import Category
from .models import Product
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.


def store(request,category_slug=None):
    if category_slug!=None:
        categories=Category.objects.get(slug=category_slug)
        products=Product.objects.filter(category=categories)
        paginator=Paginator(products,9)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
    else:
        products=Product.objects.all()
        paginator=Paginator(products,9)
        page=request.GET.get('page')
        print(page)
        paged_products=paginator.get_page(page)
        print(paged_products)
    context={
        'paginator': paginator,
        'all_products':paged_products,
        'current_category': category_slug,
    }
    return render(request,'store/store.html',context)




def search(request):
    products=[]
    if 'search' in request.GET:
        keyword=request.GET['search']
        print(keyword)
        if keyword:
            products=Product.objects.filter(Q(product_name__icontains=keyword)|Q(description__icontains=keyword))
            count=len(products)
    context={
            'all_products':products,
            

    }
    return render(request,'store/store.html',context)

def product_detail(request,category_slug=None,product_slug=None):
    categories=Category.objects.get(slug=category_slug)
    products=Product.objects.get(category=categories,slug=product_slug)
    print(products)
    
    
    context={
        'products':products
    }
    return render(request,'store/product_detail.html',context)




def rent_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        rental_days = request.POST.get('rental_days')
        # Implement the rental logic here
        return redirect('cart')  # Redirect to a success page or cart
    return render(request, 'rent_product.html', {'product': product})