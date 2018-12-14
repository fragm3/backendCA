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

# Create your views here.




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
                tranObjs = tranObjs.filter(category=category)

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
                'id':item.category,
                'label':(item.category).title()
                })
        obj['filter']['category'] = {v['id']:v for v in obj['filter']['category']}.values()
        obj['filter']['category'] = sorted(obj['filter']['category'], key=operator.itemgetter('id'))

        obj['filter']['sort_by'] = [{'id':'category','label':'Category'},
                                    {'id':'sub_category','label':'Sub Category'},
                                    {'id':'description','label':'Description'}]
        obj['filter']['order_by'] = [{'id':'asc','label':'Ascending'},
                                    {'id':'desc','label':'Descending'}]




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
        obj['filter']['sort_by'] = [{'id':'folder_name','label':'Folder Name'},
                                    {'id':'description','label':'Description'}]
        obj['filter']['order_by'] = [{'id':'asc','label':'Ascending'},
                                    {'id':'desc','label':'Descending'}]




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
        data_dict   = get_param(request, 'data_dict', [])
        if data_dict:
            data_dict = json.loads(data_dict)
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
        data_dict   = get_param(request, 'data_dict', [])
        if data_dict:
            data_dict = json.loads(data_dict)
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
        
        if data_id != None and data_id != "":
            tranObjs = Questions.objects.filter(id=data_id)
        else:
            tranObjs = Questions.objects.all()
            # Filters/Sorting Start
            if search !=None and search !="":
                tranObjs = tranObjs.filter(question_text__icontains=search)
            
            if sort_by !=None and sort_by !="" and sort_by != "none":
                if order == "asc":
                    tranObjs = tranObjs.order_by(sort_by)
                else:
                    tranObjs = tranObjs.order_by("-" + sort_by)

            if folder_id !=None and  folder_id !="" and folder_id != "none":
                tranObjs = tranObjs.filter(question_folder__id = folder_id)

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
                                    {'id':'question_type','label':'Question Type'},
                                    {'id':'topic','label':'Topic'},
                                    {'id':'difficulty_user','label':'Difficulty'},
                                    {'id':'created_at','label':'Created At'},
                                    {'id':'modified_at','label':'Modified At'},
                                    ]
        obj['filter']['order_by'] = [{'id':'asc','label':'Ascending'},
                                    {'id':'desc','label':'Descending'}]

        obj['filter']['question_type'] = [
                                    {'id':'mcq_single','label':'MCQ Single'},
                                    {'id':'mcq_multiple','label':'MCQ Multiple'},
                                    {'id':'word','label':'Word'},
                                    {'id':'number','label':'Number'},
                                    {'id':'essay','label':'Essay'},
                                    {'id':'chooseorder','label':'Choose Order'},
                                    {'id':'in_question_drop_down','label':'In Question Drop Down'},
                                    {'id':'in_question_word','label':'In Question Word'},
                                    {'id':'in_question_number','label':'In Question Number'},                                                                    
                                    ]

        obj['filter']['difficulty'] = [
                                    {'id':'1','label':'One'},
                                    {'id':'2','label':'Two'},
                                    {'id':'3','label':'Three'},
                                    {'id':'4','label':'Four'},
                                    {'id':'5','label':'Five'},
                                    {'id':'6','label':'Six'},
                                    ]

        obj['filter']['is_passage'] = [
                                    {'id':'0','label':'No'},
                                    {'id':'1','label':'Yes'},
                                    ]


    if operation == "create":  
        question_text           = get_param(request, 'question_text', None)
        question_type           = get_param(request, 'question_type', None)
        solution                = get_param(request, 'solution', None)
        topic_id                = get_param(request, 'topic_id', None)
        total_num_set_answers   = get_param(request, 'num_set', 1)
        difficulty_user         = get_param(request, 'difficulty', None)
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
            user = request.user
            try:
                folder = QuestionFolder.objects.get(id=question_folder)
            except:
                folder = None


            ts = time.time()
            created_at = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            answer_options = json.loads(answer_options)
            correct_answer = json.loads(correct_answer)            
            question = Questions.objects.create(
                question_text            = question_text,
                question_type            = question_type,
                topic                    = topic,
                total_num_set_answers    = total_num_set_answers,
                difficulty_user          = difficulty_user,
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

    if operation == "update":
        data_id                 = get_param(request, 'data_id', None)
        question_text           = get_param(request, 'question_text', None)
        question_type           = get_param(request, 'question_type', None)
        topic_id                = get_param(request, 'topic_id', None)
        total_num_set_answers   = get_param(request, 'num_set', 1)
        difficulty_user         = get_param(request, 'difficulty', None)
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
            question.difficulty_user          = difficulty_user
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
            passage_out = str(trans.passage)
        
        if trans.topic:
            topic_out = json.loads(str(trans.topic))
        else:
            topic_out = str(trans.topic)

        if trans.question_folder:
            folder_out = json.loads(str(trans.question_folder))
        else:
            folder_out = str(trans.question_folder)

        if trans.created_by:
            user_out = json.loads(str(trans.created_by))
        else:
            user_out = str(trans.created_by)


        obj['result'].append({
        'id':trans.id,
        'question_text':trans.question_text,        
        'question_type':trans.question_type,           
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
    obj['status'] = True
    return HttpResponse(json.dumps(obj), content_type='application/json')





# import boto3
# import base64

# def upload_file(request):
#     obj = {}
#     obj['status'] = False
#     obj['results'] = []
#     filetype = get_param(request, 'filetype', None)
#     bucket_name = "careeranna-media-bucket"
#     if filetype:
#         if filetype=='image':
#             obj['status'] = True
#             file = request.FILES["file"]
#             obj['filename'] = request.FILES["file"].name
#             destination = open('filename.data', 'wb')
#             for chunk in file.chunks():
#                 destination.write(chunk)
#             destination.close()
#             s3 = boto3.resource('s3')
#             s3.Object(bucket_name, 'images/test.jpg').put(Body=open('filename.data', 'rb'))
#             return HttpResponse(json.dumps(obj), content_type='application/json')










# import boto3

# some_binary_data = b'Here we have some data'
# more_binary_data = b'Here we have some more data'

# # Method 1: Object.put()
# s3 = boto3.resource('s3')
# object = s3.Object('my_bucket_name', 'my/key/including/filename.txt')
# object.put(Body=some_binary_data)

# # Method 2: Client.put_object()
# client = boto3.client('s3')
# client.put_object(Body=more_binary_data, Bucket='my_bucket_name', Key='my/key/including/anotherfilename.txt')











# LOCATION_IMAGE = 'questionmgmt/static/images'

# if settings.PRODUCTION:
#     ADDRESS = 'https://www.ipactesting.com/api/static/'
# else:
#     ADDRESS = 'http://127.0.0.1:8000/static/'
# import uuid

# def upload_file(request):
#     obj = {}
#     obj['status'] = False
#     obj['results'] = []
#     filetype = get_param(request, 'filetype', None)
#     if filetype:
#         if filetype=='image':
#             if request.method == "POST" and 'file' in request.FILES.keys():
#                 obj['status'] = True
#                 for afile in request.FILES.getlist('file'):
#                     filename = str(uuid.uuid4())+".jpg"
#                     with open(LOCATION_IMAGE+filename, 'wb+') as destination:
#                         for chunk in afile.chunks():
#                             destination.write(chunk)
#                     obj['results'].append(dict(url=ADDRESS+filename))
#                 obj['counter'] = len(obj['results'])
#                 obj['msg'] = "Success"
#                 return HttpResponse(json.dumps(obj,default=json_util.default), content_type='application/json')
#         elif filetype=='video':
#             if request.method == "POST" and 'file' in request.FILES.keys():
#                 obj['status'] = True
#                 afile = request.FILES['file']
#                 filename = str(uuid.uuid4())+".mp4"
#                 with open(LOCATION_IMAGE+filename, 'wb+') as destination:
#                     for chunk in afile.chunks():
#                         destination.write(chunk)
#                     obj['results'].append(dict(url=ADDRESS+filename))
#                 obj['counter'] = len(obj['results'])
#                 obj['msg'] = "Success"
#                 return HttpResponse(json.dumps(obj,default=json_util.default), content_type='application/json')
#     else:
#         return HttpResponseBadRequest("Bad Request")



# import requests

# cookies = {
#     '_ga': 'GA1.2.1180746591.1535354636',
#     '__auc': 'e202327f1657a448946879cce2c',
#     '__zlcmid': 'oLhdM2VSo2Mez6',
#     'ci_session': 'if3p0ubaedriupff4ee3iveb4uqo7f6d',
#     '_gid': 'GA1.2.1865445320.1544703551',
#     '__asc': '82b6b882167a781a753bec6961a',
#     '_fbp': 'fb.1.1544703552081.48840516',
#     '_gat': '1',
#     '_gat_gtag_UA_121888397_1': '1',
# }

# headers = {
#     'Pragma': 'no-cache',
#     'Origin': 'https://www.careeranna.com',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'en-US,en;q=0.9',
#     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'Accept': '*/*',
#     'Cache-Control': 'no-cache',
#     'X-Requested-With': 'XMLHttpRequest',
#     'Connection': 'keep-alive',
#     'Referer': 'https://www.careeranna.com/free-tests',
# }

# data = {
#   'phoneNumber': '1234567890',
#   'emailUser': 'dahsdiha@hdhsiuahd.com',
#   'testSlugId': 'https://www.careeranna.com/test_admin/test/test_instruction/all-india-free-cat-2018-mock-test',
#   'sourceReg': 'Free Test'
# }

# response = requests.post('https://www.careeranna.com//cuser/take_test_details', headers=headers, cookies=cookies, data=data)






# import requests

# cookies = {
#     '_ga': 'GA1.2.1180746591.1535354636',
#     '__auc': 'e202327f1657a448946879cce2c',
#     '__zlcmid': 'oLhdM2VSo2Mez6',
#     'ci_session': 'if3p0ubaedriupff4ee3iveb4uqo7f6d',
#     '_gid': 'GA1.2.1865445320.1544703551',
#     '__asc': '82b6b882167a781a753bec6961a',
#     '_fbp': 'fb.1.1544703552081.48840516',
#     '_gat': '1',
#     '_gat_gtag_UA_121888397_1': '1',
# }

# headers = {
#     'Pragma': 'no-cache',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'en-US,en;q=0.9',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
#     'Accept': 'application/json, text/javascript, */*; q=0.01',
#     'Referer': 'https://www.careeranna.com/test_admin/test/startGroupedTest/all-india-free-cat-2018-mock-test/dahsdiha@hdhsiuahd.com',
#     'X-Requested-With': 'XMLHttpRequest',
#     'Connection': 'keep-alive',
#     'Cache-Control': 'no-cache',
# }

# params = (
#     ('mode', 'test'),
#     ('answerpaper_slug', '49157'),
# )

# response = requests.get('https://www.careeranna.com/test_admin/test/testStart/cat-2018-varc-02/', headers=headers, params=params, cookies=cookies)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://www.careeranna.com/test_admin/test/testStart/cat-2018-varc-02/?mode=test&answerpaper_slug=49157', headers=headers, cookies=cookies)
