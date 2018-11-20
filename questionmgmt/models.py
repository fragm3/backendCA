from django.db import models
from djangotoolbox.fields import DictField, ListField

# Create your models here.
class Questions(models.Model):
    question_text   = models.CharField(max_length=500)
