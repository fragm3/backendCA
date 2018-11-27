from django.db import models
from djangotoolbox.fields import DictField, ListField
from usermgmt.models import CAUsers
import json


# answer_dict = dict(option_id="",option_text = "")
class Topics(models.Model):
    category     = models.CharField(max_length=50)
    sub_category = models.CharField(max_length=50)
    description  = models.CharField(max_length=300,null=True)
    def __str__(self):
        return json.dumps({'id':self.id,'category':self.category,'sub_category':self.sub_category})

class Passages(models.Model):
    header      = models.CharField(max_length=50)
    text        = models.CharField(max_length=1000)
    data_table  = ListField(DictField())
    def __str__(self):
        return json.dumps({'id':self.id,'header':self.header,'text':self.text,'data_table' : self.data_table})


# Should this be many to many mapping
class QuestionFolder(models.Model):
    folder_name = models.CharField(max_length=100)
    description  = models.CharField(max_length=300,null=True)
    def __str__(self):
        return json.dumps({'id':self.id,'category':self.folder_name})


class QuestionStructure(models.Model):
    question_text            = models.CharField(max_length=500)
    question_type            = models.CharField(max_length=50)
    # mcq_single, mcq_multiple, word, number, essay, chooseorder, in_question_drop_down, in_question_word, in_question_number
    topic                    = models.ForeignKey(Topics,
                                on_delete=models.SET_NULL,
                                null=True)
    total_num_set_answers    = models.IntegerField(default=1)
    difficulty_user          = models.IntegerField()
    to_evaluate              = models.BooleanField(default=True)
    is_passage               = models.BooleanField()
    passage                  = models.ForeignKey(Passages,
                                    on_delete=models.SET_NULL,
                                    null=True)
    num_correct_answered     = models.IntegerField(default=0)
    num_total_answered       = models.IntegerField(default=0)
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







# mcq_single, mcq_multiple, in_question_drop_down
answer_option_dict = {
    "1":[
        {"id":"1","text":"option 1"},
        {"id":"2","text":"option 2"},
        {"id":"3","text":"option 3"},
        {"id":"4","text":"option 4"},
    ]
}

correct_answer_dict = {
    "1":["1","2"]
}


# word,number, in_question_word, in_question_number
answer_option_dict = {

}

correct_answer_dict = {
    "1":"answer"
}


# essay
answer_option_dict = {

}

correct_answer_dict = {
    
}
#  chooseorder,
answer_option_dict = {
    "1":[
        {"id":"1","text":"option 1"},
        {"id":"2","text":"option 2"},
        {"id":"3","text":"option 3"},
        {"id":"4","text":"option 4"},
    ]
}
correct_answer_dict = {
    "1":["2","1","3","4"]
}








