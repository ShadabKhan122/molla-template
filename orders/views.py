
from django.shortcuts import render,redirect
from carts.models import Cart,CartItem
from .models import Order,OrderProduct,Payment
import datetime
import json
from django.http import HttpResponse,JsonResponse
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# Create your views here.
def place_order(request):
    cart_items=CartItem.objects.filter(user=request.user)
    cart_count=cart_items.count()
    if cart_count<=0:
        return redirect('store:store')
    final_total=0
    tax=0
    total=0
    quantity=0
    for cart_item in cart_items:
        total=total+(cart_item.product.price*cart_item.quantity) 
        quantity=quantity+cart_item.quantity
    tax=(8*total)/100
    final_total=total+tax
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        phone=request.POST['phone']
        email=request.POST['email']
        address_line_1=request.POST['address_line_1']
        address_line_2=request.POST['address_line_2']
        country=request.POST['country']
        state=request.POST['state']
        city=request.POST['city']
        order_note=request.POST['order_note']
        
        final_total=final_total
        print(final_total)
        tax=tax
        ip=request.META.get('REMOTE_ADDR')
        data=Order(user=request.user,first_name=first_name,last_name=last_name,phone=phone,email
              =email,address_line_1=address_line_1,address_line_2=address_line_2,country
              =country,state=state,city=city,order_note=order_note,tax=tax,order_total=final_total,ip=ip)
        data.save()
        yr=int(datetime.date.today().strftime("%Y"))
        dt=int(datetime.date.today().strftime("%d"))
        mt=int(datetime.date.today().strftime("%m"))
        d=datetime.date(yr,mt,dt)
        current_date=d.strftime("%Y%m%d")
        order_number=current_date+str(data.id)
        data.order_number=order_number
        data.save()
        order=Order.objects.get(user=request.user,is_ordered=False,order_number=order_number)
        context={
            'order':order,
            'cart_items':cart_items,
            'total':total,
            'tax':tax,
            'final_total':final_total
        }
        return render(request,'orders/payments.html',context)
    else:
        return redirect('carts:checkout')

def payments(request):
    body=json.loads(request.body)
    order=Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    payment=Payment(user=request.user,payment_id=body['transID'],payment_method=body['payment_method'],
            amount_paid=order.order_total,status=body['status'])
    payment.save()
    order.is_ordered=True
    order.payment=payment
    order.save()
    #move the cartitem to orderproduct table
    cart_items=CartItem.objects.filter(user=request.user)
    for item in cart_items:
        op=OrderProduct()
        op.order_id=order.id
        op.payment=payment
        op.user_id=request.user.id
        op.product_id=item.product.id
        op.quantity=item.quantity
        op.product_price=item.product.price
        op.ordered=True
        op.save()
        
        product=Product.objects.get(id=item.product.id)
        product.stock-=item.quantity
        product.save()
    CartItem.objects.filter(user=request.user).delete()
    mail_subject="thank you for your order"
    message=render_to_string("orders/order_received_email.html",
                             {'user':request.user,'order':order})
    to_email=request.user.email
    send_mail=EmailMessage(mail_subject,message,to=[to_email])
    send_mail.send()
    data={
        'order_number':order.order_number,
        'transID':payment.payment_id,
    }
    return JsonResponse(data)




    

def order_complete(request):
    order_number=request.GET.get('order_number')
    print(f"Order number is {order_number}")
    transID=request.GET.get('payment_id')
    print(f"Transation id {transID}")
    try:
        order=Order.objects.get(order_number=order_number,is_ordered=True)
        print(order)
        ordered_products=OrderProduct.objects.filter(order_id=order.id)
        print(ordered_products)
        total=0
        for i in ordered_products:
            total=total+i.product.price*i.quantity
        payment=Payment.objects.get(payment_id=transID)
        context={
            'order':order,
            'ordered_products':ordered_products,
            'order_number':order_number,
            'transID':payment.payment_id,
            'payment':payment,
            'total':total,
        }
        return render(request,'orders/order_complete.html',context)
    except Exception:
        return redirect('home')
        
