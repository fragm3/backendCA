from django.db import models
from djangotoolbox.fields import DictField, ListField
# from testmgmt.models import *


# answer_dict = dict(option_id='',option_text = '')

class Topic(models.Model):
    category     = models.CharField(max_length=50)
    sub_category = models.CharField(max_length=50)


class Passage(models.Model):
    total_sections     = models.IntegerField(default=1)
    section_1_header   = models.CharField(max_length=50)
    section_1_text     = models.CharField(max_length=1000)
    section_2_header   = models.CharField(max_length=50)
    section_2_text     = models.CharField(max_length=1000)
    section_3_header   = models.CharField(max_length=50)
    section_3_text     = models.CharField(max_length=1000)
    section_4_header   = models.CharField(max_length=50)
    section_4_text     = models.CharField(max_length=1000)

# Should this be many to many mapping


class Question(models.Model):
    question_text            = models.CharField(max_length=500)
    question_type            = models.CharField(max_length=50)
    # mcq_single, mcq_multiple, word, number, essay, chooseorder, drop_down
    topic                    = models.ForeignKey(Topic,
                                on_delete=models.SET_NULL,
                                null=True)
    answer_in_between        = models.BooleanField(default=False)
    total_num_set_answers    = models.IntegerField(default=1)
    difficulty_user          = models.IntegerField()
    to_evaluate              = models.BooleanField(default=True)
    is_passage               = models.BooleanField()
    passage                  = models.ForeignKey(Passage,
                                        on_delete=models.CASCADE,
                                        null=True)
    num_correct_answered     = models.IntegerField()
    num_total_answered       = models.IntegerField()
    answer_options           = ListField(DictField())
    correct_answer           = ListField(models.CharField(max_length=4))
    is_random_order          = models.BooleanField(default=False)
    # range 1 to 6
    created_at               = models.DateTimeField()
    modified_at              = models.DateTimeField()
    class Meta:
            abstract = True    


answer_options_dict = {
'set1':[
        {"id":"Shashwat Yadav","text":"Shashwat Yadav"},
        ],
    # word, number
'set2':[
         {"id":"1","text":"sample text"},
         {"id":"2","text":"sample text 2"},
         ]
    # mcq_single, mcq_multiple,  chooseorder, drop_down
}

correct_answer_dict = {
    'set1':["Shashwat Yadav"],
    # word, number
    'set2':["2","1"],
    # mcq_single, mcq_multiple,  chooseorder, drop_down
}


    # To sort value in beetween question question type


# class TestQuestions(abstractQuse):





# class Mock(models.Model):
    # name = models.CharField








