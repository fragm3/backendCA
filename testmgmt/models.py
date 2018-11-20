from django.db import models
from djangotoolbox.fields import DictField, ListField
from questionmgmt.models import *
# Create your models here.
class Test(models.Model):
    name                    = models.CharField(max_length=100)
    # test_type               = models.CharField(max_length=20)
    number_sections         = models.IntegerField()
    is_section_sequence     = models.BooleanField(default=True) 
    is_sectional_jump       = models.BooleanField(default=False)
    overall_test_time       = models.IntegerField()
    is_question_jump        = models.BooleanField(default=True)
    is_calculator           = models.BooleanField(default=False)
    is_pausable             = models.BooleanField(default=True)
    timer_type              = models.CharField(max_length=20,default="elapsed")
    # remaining / elapsed
    interface_type          = models.CharField(max_length=50,default="general")
    # General/NMAT
    num_options_mcq         = models.IntegerField(default=4)
    created_at              = models.DateTimeField()
    modified_at             = models.DateTimeField()
    edit_log                = ListField(DictField())
    

class Section(models.Model):
    name                    = models.CharField(max_length=100)
    number_questions        = models.IntegerField()
    created_at              = models.DateTimeField()
    modified_at             = models.DateTimeField()
    edit_log                = ListField(DictField())
    test                    = models.ForeignKey(Test,on_delete=models.SET_NULL,null=True)
