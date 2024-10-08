from django.db import models
from store.models import Product,Variation
from accounts.models import Account
from category.models import Category
# Create your models here.

class Wishlist(models.Model):
    wishlist_id=models.CharField(max_length=100,blank=True)
    date_add=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.wishlist_id


class WishlistItem(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True,blank=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    wishlist=models.ForeignKey(Wishlist,on_delete=models.CASCADE,null=True,blank=True)
    variation=models.ManyToManyField(Variation,blank=True)
    quantity=models.IntegerField(default=1)
    is_active=models.BooleanField(default=True) 
    def __str__(self):
        return str(self.product)
    
    def is_in_stock(self):
        return self.product.stock > 0
    
   