from django.contrib import admin
from .models import Product
from store.models import Variation
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('product_name',)}
    list_display=['product_name','slug','price','description', 'thumbnail_image1', 'thumbnail_image2', 'thumbnail_image3', 'thumbnail_image4']
admin.site.register(Product,ProductAdmin)

admin.site.register(Variation)
