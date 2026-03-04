from typing import Any

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address!")

        if not username:
            raise ValueError("User must have an username!")
        
        if not password:
            raise ValueError("Password must be provided!")
        
        email = self.normalize_email(email)
        
        user = self.model(
            username=username,
            email=email,
            full_name=full_name,
            **extra_fields
        )
        user.set_password(password)
        
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, username, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(username, email, full_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    joining_date = models.DateTimeField(default=timezone.now)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return self.username
