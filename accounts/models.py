from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
#here we are customizing admin model
class MyAccountManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        if not email:
            raise ValueError("User must have an email address")

        if not username:
            raise ValueError("user must have an username")

        user=self.model(
            email=self.normalize_email(email),
            username=username,
            
        )
        user.set_password(password)#set_passwrd()is use to set password in encrypted manner
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,username,password):

        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        
        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user
    


class Account(AbstractBaseUser):
    email=models.EmailField(max_length=100,unique=True)
    username=models.CharField(max_length=100,unique=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username',]
    def has_perm(self,perm,obj=None):
        return self.is_admin

    objects=MyAccountManager()

    def has_module_perms(self,add_label):
        return True
    def __str__(self):
        return self.email


