from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class User(AbstractUser):
    
    username = None
    email = models.EmailField(("email address"), unique=True)
    status = models.CharField(max_length = 255, default = '')
    role = models.CharField(max_length = 50, default = '')
    tag = models.CharField(max_length = 10, unique=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return '%s - %s' % (self.email, self.pk)