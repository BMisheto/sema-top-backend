from datetime import *
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.db.models import base
from email.policy import default





# User
class UserAccountManager(BaseUserManager):
    def _create_user(self, email, password,  **extra_fields):
        email = self.normalize_email(email)
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError('Password is not provided')

        user = self.model(
            email = email,
            password=password,
            **extra_fields
         )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staff(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email=email, password=password,   **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email=email, password=password,  **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True,editable=False)
    email = models.EmailField(db_index=True, unique=True, max_length=255)
    first_name = models.CharField(max_length=240,blank=True)
    last_name = models.CharField(max_length=255,blank=True)
    bio = models.CharField(max_length=120,blank=True,null=True)
    company = models.CharField(max_length=50,null=True,blank=True)
    mobile = models.CharField(max_length=250,blank=True)
    country = models.CharField(max_length=250,blank=True,default="Tanzania")
    profile_photo = models.ImageField(null=True, blank=True,default="profile.jpg",upload_to = "profile_photos")
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    


    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

        