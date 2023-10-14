from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import CustomUserManager


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=False, blank=True)
    last_login = models.DateTimeField(auto_now=True, null=False, blank=True)
    is_staff = models.BooleanField(null=False, blank=True)
    is_superuser = models.BooleanField(null=False, blank=True)

    # emai is as username here and main identifier
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()


