from django.db import models
from djangotoolbox.fields import DictField, ListField
from testmgmt.models import *

class Questions(models.Model):
    question_text   = models.CharField(max_length=500)
    





# class Mock(models.Model):
    # name = models.CharField








