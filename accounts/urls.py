# authapp/urls.py

from django.urls import path
from . import views
app_name='accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/',views.activate,name="activate"),
    path('resetpassword_validate>/<uidb64>/<token>/',views.resetpassword_validate,name="resetpassword_validate"),
    path('resetpassword/',views.resetpassword,name="resetpassword"),
    path('forgotpassword/',views.forgotpassword,name="forgotpassword"),
    path('dashboard/',views.dashboard,name="dashboard"),
]
