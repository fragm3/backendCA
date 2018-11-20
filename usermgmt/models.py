from django.db import models
from djangotoolbox.fields import DictField, ListField
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, AbstractUser
)
# Create your models here.

class CAUsers(AbstractUser):
    secret_string = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50)
    