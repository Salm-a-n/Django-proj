from django.contrib.auth.models import AbstractBaseUser, BaseUserManager 
from django.db import models 


class UserManager(BaseUserManager): 
    def create_user(self, email, password=None): 
        if not email: 
            raise ValueError("Users must have an email address") 
        email = self.normalize_email(email) 
        user = self.model(email=email) 
        user.set_password(password) 
        user.save(using=self._db) 
        return user 
    
    def create_superuser(self, email, password): 
        user = self.create_user(email, password) 
        user.is_admin = True 
        User.is_superuser = True 
        user.save(using=self._db) 
        return user 
    
class User(AbstractBaseUser): 
    email = models.EmailField(unique=True) 
    name = models.CharField(max_length =255) 
    is_active = models.BooleanField(default=True) 
    is_admin = models.BooleanField(default=False) 
    objects = UserManager() 
    
    USERNAME_FIELD = 'email'

class Recipe(models.Model):
    title=models.CharField(max_length=200)
    shef=models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients=models.TextField()
    steps=models.TextField()
    views=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    time = models.IntegerField(default=0)
    difficulty=models.CharField(max_length=50, default='Easy')
    image=models.FileField(upload_to='images/', null=True, blank=True)
    