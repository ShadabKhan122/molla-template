from django.db import models

# Create your models here.
from django.db import models
from category.models import Category
from django.urls import reverse

class ProductType(models.TextChoices):
        SETS = 'sets', 'Sets'
        TSHIRT = 'tshirt', 'T-shirt'
        SHIRT = 'shirt','shirt'
        SHOES = 'shoes','shoes'
        SWEATER = 'sweater','sweater'
        TOP = 'top','top'
        JEANS ='jeans','jeans'
        JACKET ='jacket','jacket'

class Gender(models.TextChoices):
        WOMEN = 'women', 'Women'
        MEN = 'men', 'Men'
        UNISEX = 'unisex', 'Unisex'


class Size(models.TextChoices):
        XS = 'xs', 'xs'
        S = 's', 's'
        M = 'm' , 'm'
        L = 'l', 'l'
        XL = 'xl', 'xl'
        XXL = 'xxl', 'xxl'
        
class Color(models.TextChoices):
        RED = 'red', 'Red'
        BLUE = 'blue', 'Blue'
        GREEN = 'green', 'Green'
        BLACK = 'black', 'Black'
        WHITE = 'white', 'White'
        YELLOW = 'yellow', 'Yellow'       

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=100,unique=True,)
    slug=models.SlugField(max_length=100,unique=True)
    type = models.CharField(max_length=50, choices=ProductType.choices,default=ProductType.SETS)
    gender = models.CharField(max_length=10, choices=Gender.choices,default=Gender.UNISEX)
    new = models.BooleanField(default=True)
    sale = models.BooleanField(default=False)
    top_rated = models.BooleanField(default=False)
    description=models.TextField(max_length=300,blank=True)
    price=models.IntegerField()
    rate = models.IntegerField(default=0)
    images=models.ImageField(upload_to='photos/products')
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,  null=True, blank=True, on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    brand = models.CharField(max_length=50, null=True)
    sold = models.IntegerField(default=0)
    rent_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    thumbnail_image1 = models.ImageField(upload_to='products/thumbnails/', blank=True, null=True)
    thumbnail_image2 = models.ImageField(upload_to='products/thumbnails/', blank=True, null=True)
    thumbnail_image3 = models.ImageField(upload_to='products/thumbnails/', blank=True, null=True)
    thumbnail_image4 = models.ImageField(upload_to='products/thumbnails/', blank=True, null=True)
    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('store:product_detail',args=[self.category.slug,self.slug])
    
    def is_in_stock(self):
        return self.stock > 0
    
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category="color",is_active=True)
    
    def sizes(self):
        return super(VariationManager,self).filter(variation_category="size",is_active=True)


variation_category_choice=(
    ('color','color'),
    ('size','size'),
)  

class Variation(models.Model):
    product=models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100,choices=variation_category_choice)
    variation_value=models.CharField(max_length=100)
                                     
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)
    objects=VariationManager()

    def __str__(self):
        return self.variation_value
    
