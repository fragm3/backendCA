from django.db import models
from djangotoolbox.fields import DictField, ListField
from usermgmt.models import CAUsers


# answer_dict = dict(option_id='',option_text = '')
class Topics(models.Model):
    category     = models.CharField(max_length=50)
    sub_category = models.CharField(max_length=50)
    description  = models.CharField(max_length=300,null=True)

class Passages(models.Model):
    header      = models.CharField(max_length=50)
    text        = models.CharField(max_length=1000)
    order       = models.IntegerField(default=1)
    data_table  = ListField(DictField())
    
# Should this be many to many mapping
class QuestionFolder(models.Model):
    folder_name = models.CharField(max_length=100)
    description  = models.CharField(max_length=300,null=True)

class QuestionStructure(models.Model):
    question_text            = models.CharField(max_length=500)
    question_type            = models.CharField(max_length=50)
    # mcq_single, mcq_multiple, word, number, essay, chooseorder, in_question_drop_down, in_question_word, in_question_number
    topic                    = models.ForeignKey(Topics,
                                on_delete=models.SET_NULL,
                                null=True)
    answer_in_between        = models.BooleanField(default=False)
    total_num_set_answers    = models.IntegerField(default=1)
    difficulty_user          = models.IntegerField()
    to_evaluate              = models.BooleanField(default=True)
    is_passage               = models.BooleanField()
    passage                  = models.ManyToManyField(Passages)
    num_correct_answered     = models.IntegerField()
    num_total_answered       = models.IntegerField()
    answer_options           = DictField()
    correct_answer           = DictField()
    is_random_order          = models.BooleanField(default=False)
    # range 1 to 6
    created_at               = models.DateTimeField()
    modified_at              = models.DateTimeField()
    created_by               = models.ForeignKey(CAUsers,
                                    on_delete=models.SET_NULL,
                                    null=True)
    question_folder          = models.ForeignKey(QuestionFolder,
                                                on_delete=models.SET_NULL,
                                                null=True)
    class Meta:
        abstract = True    

class Questions(QuestionStructure):
    pass






answer_options_dict = {
    '1':[
            {"id":"Shashwat Yadav","text":"Shashwat Yadav"},
        ],
    # word, number, in_question_word, in_question_number
    '2':[
         {"id":"1","text":"sample text"},
         {"id":"2","text":"sample text 2"},
         ]
    # mcq_single, mcq_multiple, chooseorder, drop_down, in_question_dropdown
}

correct_answer_dict = {
    '1':["Shashwat Yadav"],
    # word, number, in_question_word, in_question_number
    '2':["2","1"],
    # mcq_single, mcq_multiple, chooseorder, drop_down, in_question_dropdown
}









# class Mock(models.Model):
    # name = models.CharField








