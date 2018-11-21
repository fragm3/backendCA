from django.db import models
from djangotoolbox.fields import DictField, ListField
from questionmgmt.models import Question

# To Do
# 1) Test Settings Profile Creation
# 2) Profile both of section and test
# 3) Abstract Usage Correction
   
    # Can Create Test and Import as Abstract Test
    # Need to check insertion of question directly

class Instructions(models.Model):
    instruction = models.CharField(max_length=3000)
# Should this be many to many mapping with test and section


class Test(models.Model):
    name                    = models.CharField(max_length=100)
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
    # general/nmat
    num_options_mcq         = models.IntegerField(default=4)
    created_at              = models.DateTimeField()
    modified_at             = models.DateTimeField()
    edit_log                = ListField(DictField())
    is_manual               = models.BooleanField(default=False)    
    is_live                 = models.BooleanField(default=False)
    is_draft                = models.BooleanField(default=True)
    is_blank_negative       = models.BooleanField(default=False)
    blank_negative_type     = models.CharField(max_length=10)
    # sectional/overall     
    num_blank_allowed      = models.IntegerField()
    blank_negative_marks   = models.FloatField()   
    num_instructions       = models.IntegerField()


# Instructions to be added

class Section(models.Model):
    name                    = models.CharField(max_length=100)
    number_questions        = models.IntegerField()
    section_time            = models.IntegerField()
    created_at              = models.DateTimeField()
    modified_at             = models.DateTimeField()
    edit_log                = ListField(DictField())
    # Blank Marks Handling
    is_blank_negative       = models.BooleanField(default=False)
    num_blank_allowed       = models.IntegerField()
    blank_negative_marks    = models.FloatField()    
    is_instruction          = models.BooleanField(default=False)
    instructions            = models.ForeignKey(Instructions,
                                                on_delete=models.SET_NULL,
                                                null=True)
    test                    = models.ForeignKey(Test,
                                                on_delete=models.SET_NULL,
                                                null=True)

class SectionQuestions(Question):
    positive_marks = models.FloatField()
    negative_marks = models.FloatField()
    section  = models.ForeignKey(Section,
                                    on_delete=models.CASCADE,
                                    null=True)
    question = models.ForeignKey(Question,
                                    on_delete=models.SET_NULL,
                                    null=True)




