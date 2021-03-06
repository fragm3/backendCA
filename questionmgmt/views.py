from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponseForbidden,HttpResponse
from django.core.paginator import Paginator
from django.core import serializers
from models import *
from django.db.models import Q
from overall.views import get_param,cleanstring
import math
import json
import time
from datetime import datetime
from testmgmt.models import SectionQuestions
import operator
from fuzzywuzzy import fuzz
# Create your views here.

question_types = {
                  'mcq_single':'MCQ Single',
                  'mcq_multiple':'MCQ Multiple',
                  'word':'Word',
                  'number':'Number',
                  'essay':'Essay',
                  'chooseorder':'Choose Order',
                  'in_question_drop_down':'In Question Drop Down',
                  'in_question_word':'In Question Word',
                  'in_question_number':'In Question Number',                                                                    
                  }

question_types_list = [
                 'mcq_single'
                ,'mcq_multiple'
                ,'word'
                ,'number'
                ,'essay'
                ,'chooseorder'
                ,'in_question_drop_down'
                ,'in_question_word'
                ,'in_question_number'
                ]

difficulty_types_list = [
                 '1'
                ,'2'
                ,'3'
                ,'4'
                ,'5'
                ,'6']



def crud_topics(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    obj['message'] = "Request Recieved"
    obj['filter'] = {}
    operation = get_param(request, 'operation', "read")
    tranObjs = []
    if operation == "read":
        page_num = get_param(request, 'page_num', None)
        page_size = get_param(request, 'page_size', None)
        data_id = get_param(request,'data_id',None)   
        search = get_param(request,'search',None) 
        sort_by = get_param(request,'sort_by',None) 
        category = get_param(request,'category',None) 
        order = get_param(request,'order_by',None) 

        if data_id != None and data_id != "":
            tranObjs = Topics.objects.filter(id=data_id)
        else:
            tranObjs = Topics.objects.all().order_by('category')
            # Filters/Sorting Start

            if category !=None and category !="" and category != "none":
                category_list = category.split(",")
                tranObjs = tranObjs.filter(category__in=category_list)

            if search !=None and search !="":
                tranObjs = tranObjs.filter(Q(category__icontains=search) | Q(sub_category__icontains=search) | Q(description__icontains=search))
            
            if sort_by !=None and sort_by !="" and sort_by !="none":
                if order == "asc":
                        tranObjs = tranObjs.order_by(sort_by)
                else:
                    tranObjs = tranObjs.order_by("-" + sort_by)


            # Filters/Sorting End
        # pagination variable
        num_pages = 1
        total_records = tranObjs.count()    
        if page_num != None and page_num != "":
            page_num = int(page_num)
            tranObjs = Paginator(tranObjs, int(page_size))
            try:
                tranObjs = tranObjs.page(page_num)
            except:
                tranObjs = tranObjs
            num_pages = int(math.ceil(total_records / float(int(page_size))))
        # data = list(tranObjs)
        obj['message'] = "Success"
        obj['num_pages'] = num_pages
        obj['total_records'] = total_records

        category_list = Topics.objects.all()
        obj['filter']['category'] = []
        for item in category_list:
            obj['filter']['category'].append({
                'value':item.category,
                'label':(item.category).title()
                })
        obj['filter']['category'] = {v['value']:v for v in obj['filter']['category']}.values()
        obj['filter']['category'] = sorted(obj['filter']['category'], key=operator.itemgetter('value'))

        obj['filter']['sort_by'] = [{'value':'','label':'None'},
                                    {'value':'category','label':'Category'},
                                    {'value':'sub_category','label':'Sub Category'},
                                    {'value':'description','label':'Description'}]
        obj['filter']['order_by'] = [{'value':'asc','label':'Ascending'},
                                    {'value':'desc','label':'Descending'}]

    if operation == "create":
        category     = get_param(request, 'category', None)
        sub_category = get_param(request, 'subcategory', None)
        description  = get_param(request,'desc',None)

        category     = cleanstring(category).lower()
        sub_category = cleanstring(sub_category).lower()
        description  = cleanstring(description)
        tranObjs     = Topics.objects.filter(category=category,sub_category=sub_category)

        if len(tranObjs):
            obj['message'] = "Topic Already Exists!"
        else:
            topic = Topics.objects.create(category=category,sub_category=sub_category,description=description)
            tranObjs = [topic]
            obj['message'] = "Topic Created"

    if operation == "update":
        data_id      = get_param(request, 'data_id', None)

        category     = get_param(request, 'category', None)
        sub_category = get_param(request, 'subcategory', None)
        description  = get_param(request,'desc',None)

        category = cleanstring(category).lower()
        sub_category = cleanstring(sub_category).lower()
        description = cleanstring(description).lower()
        try:
            topic = Topics.objects.get(id=data_id)
        except:
            topic = None
        obj['message'] = "Topic Not Found"
        if topic:
            topic.category = category
            topic.sub_category = sub_category
            topic.description = description
            topic.save()
            tranObjs = [topic]
            obj['message'] = "Topic Updated"
        
    if operation == "delete":
        data_id      = get_param(request, 'data_id', None)
        try:
            topic = Topics.objects.get(id=data_id)
        except:
            topic = None
        obj['message'] = "Topic Not Found"        
        if topic:
            topic.delete()
            obj['message'] = "Topic Deleted"

    for trans in tranObjs:
        obj['result'].append({
        'id':trans.id,
        'category':trans.category,
        'sub_category':trans.sub_category,
        'description':trans.description
    })
    obj['status'] = True
    return HttpResponse(json.dumps(obj), content_type='application/json')

def crud_folders(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    obj['message'] = "Request Recieved"
    obj['filter'] = {}
    tranObjs = []
    operation = get_param(request, 'operation', "read")
    if operation == "read":
        tranObjs = None
        page_num = get_param(request, 'page_num', None)
        page_size = get_param(request, 'page_size', None)
        data_id = get_param(request,'data_id',None)    
        search = get_param(request,'search',None) 
        sort_by = get_param(request,'sort_by',None) 
        order = get_param(request,'order_by',None)    
        if data_id != None and data_id != "":
            tranObjs = QuestionFolder.objects.filter(id=data_id)
        else:
            tranObjs = QuestionFolder.objects.all().order_by('folder_name')
            # Filters/Sorting Start
            if search !=None and search !="":
                tranObjs = tranObjs.filter(Q(folder_name__icontains=search) | Q(description__icontains=search))
            
            if sort_by !=None and sort_by !="" and sort_by != "none":
                if order == "asc":
                    tranObjs = tranObjs.order_by(sort_by)
                else:
                    tranObjs = tranObjs.order_by("-" + sort_by)
            # Filters/Sorting End
        # pagination variable
        num_pages = 1
        total_records = tranObjs.count()    
        if page_num != None and page_num != "":
            page_num = int(page_num)
            tranObjs = Paginator(tranObjs, int(page_size))
            try:
                tranObjs = tranObjs.page(page_num)
            except:
                tranObjs = tranObjs
            num_pages = int(math.ceil(total_records / float(int(page_size))))
        # data = list(tranObjs)
        obj['message'] = "Success"
        obj['num_pages'] = num_pages
        obj['total_records'] = total_records
        obj['filter']['sort_by'] = [
                                    {'value':'','label':'None'},
                                    {'value':'folder_name','label':'Folder Name'},
                                    {'value':'description','label':'Description'}]
        obj['filter']['order_by'] = [{'value':'asc','label':'Ascending'},
                                    {'value':'desc','label':'Descending'}]




    if operation == "create":
        folder_name  = get_param(request, 'folder_name', None)
        description  = get_param(request,'desc',None)
        folder_name  = cleanstring(folder_name)
        description  = cleanstring(description)

        tranObjs     = QuestionFolder.objects.filter(folder_name=folder_name)

        if len(tranObjs):
            obj['message'] = "Folder Already Exists!"
        else:
            folder = QuestionFolder.objects.create(folder_name=folder_name,description=description)
            tranObjs = [folder]
            obj['message'] = "Folder Created"

    if operation == "update":
        data_id      = get_param(request, 'data_id', None)
        folder_name  = get_param(request, 'folder_name', None)
        description  = get_param(request,'desc',None)

        folder_name  = cleanstring(folder_name)
        description  = cleanstring(description)
        try:
            folder = QuestionFolder.objects.get(id=data_id)
        except:
            folder = None
        obj['message'] = "Folder Not Found"
        if folder:
            folder.folder_name = folder_name
            folder.description = description
            folder.save()
            tranObjs = [folder]
            obj['message'] = "Folder Updated"

    if operation == "delete":
        data_id      = get_param(request, 'data_id', None)
        try:
            folder  = QuestionFolder.objects.get(id=data_id)
        except:
            folder = None
        obj['message'] = "Folder Not Found"
        if folder:
            folder.delete()
            obj['message'] = "Folder Deleted"

    for trans in tranObjs:
        obj['result'].append({
        'id':trans.id,
        'folder_name':trans.folder_name,
        'description':trans.description
    })
    obj['status'] = True
    return HttpResponse(json.dumps(obj), content_type='application/json')

# Query Correction at deletion pending 
def crud_passages(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    obj['message'] = "Request Recieved"
    obj['filter'] = {}
    operation = get_param(request, 'operation', "read")
    tranObjs = []
    if operation == "read":
        page_num = get_param(request, 'page_num', None)
        page_size = get_param(request, 'page_size', None)
        data_id = get_param(request,'data_id',None)    
        if data_id != None and data_id != "":
            tranObjs = Passages.objects.filter(id=data_id)
        else:
            tranObjs = Passages.objects.all()
            # Filters/Sorting Start
        
            # Filters/Sorting End
        # pagination variable
        num_pages = 1
        total_records = tranObjs.count()    
        if page_num != None and page_num != "":
            page_num = int(page_num)
            tranObjs = Paginator(tranObjs, int(page_size))
            try:
                tranObjs = tranObjs.page(page_num)
            except:
                tranObjs = tranObjs
            num_pages = int(math.ceil(total_records / float(int(page_size))))
        # data = list(tranObjs)
        obj['message'] = "Success"
        obj['num_pages'] = num_pages
        obj['total_records'] = total_records

    if operation == "create":
        header      = get_param(request, 'header', None)
        text        = get_param(request, 'text', None)
        data_dict   = get_param(request, 'data_dict', None)
        if data_dict:
            if len(data_dict):
                 data_dict = json.loads(data_dict)
        else:
            data_dict = []

        tranObjs     = Passages.objects.filter(header=header,text=text)

        if len(tranObjs):
            obj['message'] = "Passage Already Exists!"
        else:
            passage = Passages.objects.create(header=header,text=text,data_table=data_dict)
            tranObjs = [passage]
            obj['message'] = "Passage Created"

    if operation == "update":
        data_id      = get_param(request, 'data_id', None)
        header      = get_param(request, 'header', None)
        text        = get_param(request, 'text', None)
        data_dict   = get_param(request, 'data_dict', None)
        if data_dict:
            if len(data_dict):
                data_dict = json.loads(data_dict)
        else:
            data_dict = []
        try:         
            passage = Passages.objects.get(id=data_id)
        except:
            passage = None
        obj['message'] = "Passage Not Found"
        if passage:
            passage.header = header
            passage.text = text
            passage.data_table = data_dict
            passage.save()
            tranObjs = [passage]
            obj['message'] = "Passage Updated"

    if operation == "delete":
        data_id      = get_param(request, 'data_id', None)
        try:     
            passage = Passages.objects.get(id=data_id)
        except:
            passage = None
        obj['message'] = "Passage Not Found"        
        if passage:
            questions_linked = passage.questions_set.all()
            try:
                print len(questions_linked)
                if questions_linked:
                    obj['message'] = "Passage Linked To Questions Can't Be Deleted"
                    # To Be Checked After Question Add
                else:
                    passage.delete()
                    obj['message'] = "Passage Deleted"
            except:
                    passage.delete()
                    obj['message'] = "Passage Deleted"

    for trans in tranObjs:
        obj['result'].append({
        'id':trans.id,
        'header':trans.header,
        'text':trans.text,
        'data_table':trans.data_table
    })
    obj['status'] = True
    return HttpResponse(json.dumps(obj), content_type='application/json')


# Query Correction at deletion pending 

# Answer Dict/ Options Dict Check Addition
def crud_questions(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    obj['message'] = "Request Recieved"
    obj['filter'] = {}
    operation = get_param(request, 'operation', "read")
    tranObjs = []
    if operation == "read":
        page_num = get_param(request, 'page_num', None)
        page_size = get_param(request, 'page_size', None)
        data_id = get_param(request,'data_id',None)   
        folder_id = get_param(request,'folder_id',None)    
        search = get_param(request,'search',None)    
        sort_by = get_param(request,'sort_by',None)    
        order = get_param(request,'order_by',None)   
        question_type = get_param(request,'question_type',None)   
        difficulty = get_param(request,'difficulty',None)   
        is_passage = get_param(request,'is_passage',None)   
        is_random = get_param(request,'is_random',None)   
        topic_id = get_param(request,'topic_id',None)   

        if data_id != None and data_id != "":
            tranObjs = Questions.objects.filter(id=data_id)
        else:
            tranObjs = Questions.objects.all()
            # Filters/Sorting Start
            if folder_id !=None and  folder_id !="" and folder_id != "none":
                folder_id_list = folder_id.split(",")
                tranObjs = tranObjs.filter(question_folder__id__in = folder_id_list)

            if search !=None and search !=""  and search != "none":
                tranObjs = tranObjs.filter(question_text__icontains=search)
            
            if sort_by !=None and sort_by !="" and sort_by != "none":
                if order == "asc":
                    tranObjs = tranObjs.order_by(sort_by)
                else:
                    tranObjs = tranObjs.order_by("-" + sort_by)

            if question_type !=None and question_type !=""  and question_type != "none":
                print "test"
                question_type_list = question_type.split(",")
                tranObjs = tranObjs.filter(question_type__in=question_type_list)

            if difficulty !=None and difficulty !=""  and difficulty != "none":
                difficulty_list = difficulty.split(",")
                difficulty_list = map(lambda x : int(x),difficulty_list)
                tranObjs = tranObjs.filter(difficulty_user__in=difficulty_list)

            if is_passage !=None and is_passage !=""  and is_passage != "none":
                if is_passage == "1":
                    tranObjs = tranObjs.filter(is_passage=True)
                else:
                    tranObjs = tranObjs.filter(is_passage=False)

            if is_random !=None and is_random !=""  and is_random != "none":
                if is_random == "1":
                    tranObjs = tranObjs.filter(is_random_order=True)
                else:
                    tranObjs = tranObjs.filter(is_random_order=False)

            if topic_id !=None and topic_id !=""  and topic_id != "none":
                topic_id_list = topic_id.split(",")
                print "here"
                tranObjs = tranObjs.filter(topic__id__in = topic_id_list)



            # Filters/Sorting End
        # pagination variable
        num_pages = 1
        total_records = tranObjs.count()    
        if page_num != None and page_num != "":
            page_num = int(page_num)
            tranObjs = Paginator(tranObjs, int(page_size))
            try:
                tranObjs = tranObjs.page(page_num)
            except:
                tranObjs = tranObjs
            num_pages = int(math.ceil(total_records / float(int(page_size))))
        # data = list(tranObjs)
        obj['message'] = "Success"
        obj['num_pages'] = num_pages
        obj['total_records'] = total_records
        obj['filter']['sort_by'] = [{'value':'','label':'None'},
                                    {'value':'question_type','label':'Question Type'},
                                    {'value':'topic','label':'Topic'},
                                    {'value':'difficulty_user','label':'Difficulty'},
                                    {'value':'created_at','label':'Created At'},
                                    {'value':'modified_at','label':'Modified At'},
                                    ]

        obj['filter']['order_by'] = [{'value':'asc','label':'Ascending'},
                                    {'value':'desc','label':'Descending'}]
        obj['filter']['question_type'] = []

        for ques_type in question_types_list:
            obj['filter']['question_type'].append({'value':ques_type,'label':question_types[ques_type]})

        obj['filter']['difficulty'] = [
                                    {'value':'1','label':'1'},
                                    {'value':'2','label':'2'},
                                    {'value':'3','label':'3'},
                                    {'value':'4','label':'4'},
                                    {'value':'5','label':'5'},
                                    {'value':'6','label':'6'},
                                    ]

        obj['filter']['is_passage'] = [{'value':'','label':'None'},
                                    {'value':'0','label':'No'},
                                    {'value':'1','label':'Yes'},
                                    ]

        obj['filter']['is_random'] = [{'value':'','label':'None'},
                                    {'value':'0','label':'No'},
                                    {'value':'1','label':'Yes'},
                                    ]
        
        obj['filter']['topics'] = []
        topics = Topics.objects.all()
        for topic in topics:
            obj['filter']['topics'].append({
                'value':topic.id,
                'label':topic.category + " - " + topic.sub_category
            })
        obj['filter']['folders'] = []
        folders = QuestionFolder.objects.all()
        for folder in folders:
            obj['filter']['folders'].append({
                'value':folder.id,
                'label':folder.folder_name
            })


        obj['filter']['to_evaluate'] = [{'value':'','label':'None'},
                                    {'value':'0','label':'No'},
                                    {'value':'1','label':'Yes'},
                                    ]


    if operation == "create":  
        question_text           = get_param(request, 'question_text', None)
        question_type           = get_param(request, 'question_type', None)
        solution                = get_param(request, 'solution', None)
        topic_id                = get_param(request, 'topic_id', None)
        total_num_set_answers   = get_param(request, 'num_set', 1)
        difficulty_user         = get_param(request, 'difficulty', "1")
        to_evaluate             = get_param(request, 'to_evaluate', "1")
        is_passage              = get_param(request, 'is_passage', "1")
        passage_id              = get_param(request, 'passage_id', None)
        answer_options          = get_param(request,'option_dict',None)
        correct_answer          = get_param(request,'correct_dict',None)
        is_random_order         = get_param(request,'is_random',"0")
        question_folder         = get_param(request,'folder_id',None)

        tranObjs     = Questions.objects.filter(question_text=question_text,question_type=question_type)
        if len(tranObjs):
            obj['message'] = "Question Already Exists!"
        else:
            try:
                topic = Topics.objects.get(id=topic_id)
            except:
                topic = None
                
            if is_passage == "1":
                is_passage = True
            else:
                is_passage = False

            if to_evaluate == "1":
                to_evaluate = True
            else:
                to_evaluate = False

            if is_random_order == "1":
                is_random_order = True
            else:
                is_random_order = False


            if is_passage:
                passage = Passages.objects.get(id=passage_id)
            else:
                passage = None
            if request.user.is_anonymous:
                user = None
            else:
                user = request.user
            try:
                folder = QuestionFolder.objects.get(id=question_folder)
            except:
                folder = None

            if difficulty_user not in difficulty_types_list:
                difficulty_user = "0"

            
            ts = time.time()
            created_at = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            answer_options = json.loads(answer_options)
            correct_answer = json.loads(correct_answer)            
            if question_type in question_types_list:
                question = Questions.objects.create(
                    question_text            = question_text,
                    question_type            = question_type,
                    topic                    = topic,
                    total_num_set_answers    = total_num_set_answers,
                    difficulty_user          = int(difficulty_user),
                    to_evaluate              = to_evaluate,
                    solution                 = solution,
                    is_passage               = is_passage,
                    passage                  = passage,
                    answer_options           = answer_options,
                    correct_answer           = correct_answer,
                    is_random_order          = is_random_order,
                    created_at               = created_at,
                    modified_at              = created_at,
                    created_by               = user,
                    question_folder          = folder,
                )
                tranObjs = [question]
                obj['message'] = "Question Created"
            else:
                obj['message'] = "Incorrect Question Type"

    if operation == "update":
        data_id                 = get_param(request, 'data_id', None)
        question_text           = get_param(request, 'question_text', None)
        question_type           = get_param(request, 'question_type', None)
        topic_id                = get_param(request, 'topic_id', None)
        total_num_set_answers   = get_param(request, 'num_set', 1)
        difficulty_user         = get_param(request, 'difficulty', "0")
        to_evaluate             = get_param(request, 'to_evaluate', True)
        is_passage              = get_param(request, 'is_passage', True)
        solution                = get_param(request, 'solution', None)
        passage_id              = get_param(request, 'passage_id', True)
        answer_options          = get_param(request,'option_dict',None)
        correct_answer          = get_param(request,'correct_dict',None)
        is_random_order         = get_param(request,'is_random',False)
        question_folder         = get_param(request,'folder_id',None)

        try:
            question = Questions.objects.get(id=data_id)
        except:
            question = None
        obj['message'] = "Question Not Found"
        if question:
            

            if difficulty_user not in difficulty_types_list:
                difficulty_user = "0"

            if is_passage == "1":
                is_passage = True
            else:
                is_passage = False

            if to_evaluate == "1":
                to_evaluate = True
            else:
                to_evaluate = False

            if is_random_order == "1":
                is_random_order = True
            else:
                is_random_order = False

            try:
                topic = Topics.objects.get(id=topic_id)
            except:
                topic = None
            
            
            if is_passage:
                passage = Passages.objects.get(id=passage_id)
            else:
                passage = None
    
            ts = time.time()
            modified_at = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            try:
                folder = QuestionFolder.objects.get(id=question_folder)
            except:
                folder = None            
            question.question_text            = question_text
            question.question_type            = question_type
            question.topic                    = topic
            question.total_num_set_answers    = total_num_set_answers
            question.difficulty_user          = int(difficulty_user)
            question.to_evaluate              = to_evaluate
            question.is_passage               = is_passage
            question.solution                 = solution
            question.passage                  = passage
            question.answer_options           = json.loads(answer_options)
            question.correct_answer           = json.loads(correct_answer)
            question.is_random_order          = is_random_order
            question.modified_at              = modified_at
            question.question_folder          = folder
            question.save()
            tranObjs = [question]
            obj['message'] = "Question Updated"

    if operation == "delete":
        data_id      = get_param(request, 'data_id', None)
        try:
            question = Questions.objects.get(id=data_id)
        except:
            question = None

        obj['message'] = "Question Not Found"        
        if question:
            questions_linked = question.sectionquestions_set.all()
            try:
                print len(questions_linked)
                if questions_linked:
                    obj['message'] = "Question Linked To Tests Can't Be Deleted"
                    # To Be Checked After Question Add
                else:
                    question.delete()
                    obj['message'] = "Question Deleted"
            except:
                    question.delete()
                    obj['message'] = "Question Deleted"

    for trans in tranObjs:
        if trans.passage:
            passage_out = json.loads(str(trans.passage))
        else:
            passage_out = json.loads(str(json.dumps({'id':'','header':'','text':'','data_table' : []})))
        
        if trans.topic:
            topic_out = json.loads(str(trans.topic))
        else:
            topic_out = json.loads(str(json.dumps({'id':'','category':'','sub_category':''})))

        if trans.question_folder:
            folder_out = json.loads(str(trans.question_folder))
        else:
            folder_out = json.loads(str(json.dumps({'id':'','folder_name':''})))

        if trans.created_by:
            user_out = json.loads(str(trans.created_by))
        else:
            user_out = json.loads(str(json.dumps({'id':'','first_name':'' ,'last_name':'','email':''})))

        try:
            obj['result'].append({
            'id':trans.id,
            'question_text':trans.question_text,        
            'question_type':{"value":trans.question_type,"label":question_types[trans.question_type]},           
            # 'topic': serializers.serialize("json", trans.topic),          
            'topic': topic_out,          
            'total_num_set_answers':trans.total_num_set_answers,    
            'difficulty_user':trans.difficulty_user,   
            'to_evaluate':trans.to_evaluate,  
            'solution':trans.solution,  
            'is_passage':trans.is_passage, 
            'passage':passage_out,
            'num_correct_answered':trans.num_correct_answered,
            'num_total_answered':trans.num_total_answered,
            'answer_options':trans.answer_options,
            'correct_answer':trans.correct_answer,
            'is_random_order':trans.is_random_order,
            'created_at':str(trans.created_at),
            'modified_at':str(trans.modified_at),
            'created_by':user_out,
            'question_folder':folder_out         
        })
        except:
            None
    obj['status'] = True
    return HttpResponse(json.dumps(obj), content_type='application/json')

# def check_answer_dict(question_type,option_dict,answer_dict,total_num_set_answers):
#     obj = {}
#     obj['message'] = "Check Start"
#     obj['allowed'] = False
#     if question_type in ['mcq_single','mcq_multiple','in_question_drop_down']:
#         for num in range(1,num_question_set+1):
#             try:
#                 answer_dictionary_check = answer_dict[str(num)]
#                 obj['message'] = "Dictionary Correct"
#                 try:
#                     if len(answer_dictionary_check) >= 1:
#                         for val in answer_dictionary_check:
#                             obj['message'] = "Dictionary Correct"
#                     else:
#                         obj['message'] = "Values Present Correct"
#                 except:
#                     obj['message'] = "Options values not passed as list"
    
#             except:
#                 obj['message'] = "Dictionary Incorrect"
#                 return obj


#                 if res not in question.correct_answer[str(num)]:
#                     answer_options = False
#             if len(response[str(num)]) != len(question.correct_answer[str(num)]):
#                 answer_len = False



def check_api(request):
    check = get_param(request, 'check', None)
    if check:
        check = 1
    return HttpResponse(json.dumps(check), content_type='application/json')


def check_answer(question,response):
    answer = True
    answer_options = True
    answer_len  = True
    num_question_set = question.total_num_set_answers
    if question.question_type in ['mcq_single','mcq_multiple','in_question_drop_down']:
        for num in range(1,num_question_set+1):
            for res in response[str(num)]:
                if res not in question.correct_answer[str(num)]:
                    answer_options = False
            if len(response[str(num)]) != len(question.correct_answer[str(num)]):
                answer_len = False
            
        answer = (answer_options and answer_len)
                    
    if question.question_type in ['word','in_question_word']:
         for num in range(1,num_question_set+1):
            res = response[str(num)]
            if fuzz.ratio(res.lower(), question.correct_answer[str(num)].lower()) <= 90:
                answer = False

    if question.question_type in ['number','in_question_number']:
         for num in range(1,num_question_set+1):
            res = response[str(num)]
            if float(res) != float(question.correct_answer[str(num)]):
                answer = False

    if question.question_type in ['chooseorder']:
        for num in range(1,num_question_set+1):
            if response[str(num)] != question.correct_answer[str(num)]:
                answer = False
    return answer

def check_answer_api(request):
    obj = {}
    obj['status'] = False
    obj['result'] = {
                    "answer":False
                    }
    obj['message'] = "Request Recieved"
    question_id = get_param(request, 'q_id', None)   
    qresponse = get_param(request, 'qresponse', None)   
    qtype = get_param(request, 'qtype', None)   
    if_correct = True

    if qtype == "individual":
        try:
            question = Questions.objects.get(id=question_id)
            message = "Question Found"
        except:
            message = "Question Not Found"
    
    if qtype == "test":
        try:
            question = Questions.objects.get(id=question_id)
            message = "Question Found"
        except:
            message = "Question not Found"
    
    if question:
        if question.to_evaluate and question.question_type != "essay":
            message = "Evaluation Possible"
            try:
                if_correct = check_answer(question=question,response=json.loads(qresponse))
                message = "Success!"
            except:
                message = "Error in Evaluation"
        else:
            message = "Evaluation not Possible"

    obj['message'] = message
    obj['status'] = True
    obj['result'] = {'answer':if_correct}
    return HttpResponse(json.dumps(obj), content_type='application/json')


