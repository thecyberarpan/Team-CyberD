from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import *

# create your models here

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=14)
    is_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length = 200, null=True, blank=True)
    forgot_password = models.CharField(max_length = 100, null=True,blank=True)
    last_login_time = models.DateTimeField(null = True, blank = True)
    lats_logout_time = models.DateTimeField(null = True, blank = True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    