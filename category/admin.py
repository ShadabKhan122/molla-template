from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('category_name',)}
    list_display=['category_name','slug','description','image']

admin.site.register(Category,CategoryAdmin)