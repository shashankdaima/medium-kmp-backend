from django.db import models
from django.contrib.auth.models import AbstractUser
from .user_manager import UserManager
# Create your models here.
class User(AbstractUser):
    created_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_banned = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=256,unique=True )
    username=None

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["password"]

    objects=UserManager()

    def __str__(self):
        return self.email
    