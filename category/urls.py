from django.urls import path
from molla.views import sales,featured,rated
from .views import home
urlpatterns = [
    path('', home, name='home'),
    
    path('featured/', featured, name='featured'),
    path('sale/', sales, name='sales'),
    path('rated/', rated, name='rated'),
]
