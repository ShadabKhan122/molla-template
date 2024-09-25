from django.db import models
from accounts.models import Account
from store.models import Variation
# Create your models here.
from store.models import Product
class Cart(models.Model):
    cart_id=models.CharField(max_length=100,blank=True)
    date_added=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True,blank=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True,blank=True)
    variation=models.ManyToManyField(Variation,blank=True)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)
    rental_days = models.IntegerField(default=0) 

    def sub_total(self):
        return self.product.price*self.quantity
 
    def __str__(self):
        return str(self.product)
    
    def rent_total(self):
        return self.product.rent_per_day * self.rental_days * self.quantity