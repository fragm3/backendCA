from django.db import models
from djangotoolbox.fields import DictField, ListField
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, AbstractUser
)
# Create your models here.

class CAUsers(AbstractUser):
    secret_string = models.CharField(max_length=20, null=True)
    auth_token = models.CharField(max_length=20, null=True)
    # phone_number = models.CharField(max_length=50)
    is_admin    = models.BooleanField(default=False)
    is_manager    = models.BooleanField(default=False)




    