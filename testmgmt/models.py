from django.db import models
from djangotoolbox.fields import DictField, ListField
from questionmgmt.models import QuestionStructure,Questions
from usermgmt.models import CAUsers
# To Do

# 1) Test Settings Profile Creation
# 2) Profile both of section and test - Dropdown of profile
# 3) Abstract Usage Correction
# 4) Admin Panel All Courses Visible
# 5) User Side Bought Courses Visible
# Question Category and Test Category Implementation
# Active Tests
# Inactive Tests
# Preview Test to be deleted at the end
# Last non correct option to be deleted in MCQ 
# Test Scheduling Variable
# Question Flagging Variables
# Test Creater Summary

# Can Create Test and Import as Abstract Test
# Need to check insertion of question directl
# 
# Should instructions be many to many mapping with test and section
# To resolve order of display y

# Instructions Database

# Admin


# Not Yet Started
# In Progress
# Finish


# Is Live

# Test Live on the system

# Test Categories
    # Overall 
    # Section
    # Topic Wise

# Sectional Categories

class Instructions(models.Model):
    instruction = models.CharField(max_length=3000)
    order       = models.IntegerField()

# Genric Profile of Test
class TestStructure(models.Model):
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
    is_eval_manual          = models.BooleanField(default=False)    
    is_blank_negative       = models.BooleanField(default=False)
    blank_negative_type     = models.CharField(max_length=10)
    # sectional/overall     
    num_blank_allowed      = models.IntegerField()
    blank_negative_marks   = models.FloatField()   
    num_instructions       = models.IntegerField()
    class Meta:
        abstract= True


# Generic Profile of section
class SectionStructure(models.Model):
    number_questions        = models.IntegerField()
    section_time            = models.IntegerField()
    # Blank Marks Handling
    is_blank_negative       = models.BooleanField(default=False)
    num_blank_allowed       = models.IntegerField()
    blank_negative_marks    = models.FloatField()    
    is_instruction          = models.BooleanField(default=False)
    instruction             = models.ForeignKey(Instructions,
                                                on_delete=models.SET_NULL,
                                                null=True)
    class Meta:
        abstract = True

class TestFolder(models.Model):
    folder_name = models.CharField(max_length=100)

class Tests(TestStructure):
    test_name               = models.CharField(max_length=100)
    is_live_draft           = models.BooleanField(default=False)
    status                  = models.CharField(max_length=10)
    created_at              = models.DateTimeField()
    modified_at             = models.DateTimeField()
    edit_log                = ListField(DictField())
    scheduled_for           = models.DateTimeField()
    comments                = models.CharField(max_length=200)
    instructions            = models.ManyToManyField(Instructions) 
    folder                  = models.ForeignKey(TestFolder,
                                                on_delete=models.SET_NULL,
                                                null = True)
    created_by              = models.ForeignKey(CAUsers,
                                                on_delete=models.SET_NULL,
                                                null=True)
    def __str__(self):
        return self.test_name
    
    

class Section(SectionStructure):
    name                    = models.CharField(max_length=100)
    created_at              = models.DateTimeField()
    modified_at             = models.DateTimeField()
    edit_log                = ListField(DictField())
    test                    = models.ForeignKey(Tests,
                                                on_delete=models.SET_NULL,
                                                null=True)
    created_by              = models.ForeignKey(CAUsers,
                                                on_delete=models.SET_NULL,
                                                null=True)


class TestProfile(TestStructure):
    profile_name            = models.CharField(max_length=100)
    created_at              = models.DateTimeField()
    modified_at             = models.DateTimeField()
    edit_log                = ListField(DictField())
    created_by              = models.ForeignKey(CAUsers,
                                                on_delete=models.SET_NULL,
                                                null=True)

class SectionProfile(SectionStructure):
    name                    = models.CharField(max_length=100)
    created_at              = models.DateTimeField()
    modified_at             = models.DateTimeField()
    edit_log                = ListField(DictField())
    testprofile             = models.ForeignKey(TestProfile,
                                                on_delete=models.SET_NULL,
                                                null=True)




# Instructions to be added

class SectionQuestions(QuestionStructure):
    positive_marks = models.FloatField()
    negative_marks = models.FloatField()
    section  = models.ForeignKey(Section,
                                on_delete=models.CASCADE,
                                null=True)                            
    question = models.ForeignKey(Questions,
                                    on_delete=models.SET_NULL,
                                    null=True)




