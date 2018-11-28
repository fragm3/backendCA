from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponseForbidden,HttpResponse
from django.core.paginator import Paginator
from django.core import serializers
from models import *
from overall.views import get_param,cleanstring
import math
import json
import time
from datetime import datetime
from testmgmt.models import SectionQuestions

@csrf_exempt
# Create your views here.

def crud_topics(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    obj['message'] = "Request Recieved"
    operation = get_param(request, 'operation', "read")
    tranObjs = []
    if operation == "read":
        page_num = get_param(request, 'page_num', None)
        page_size = get_param(request, 'page_size', None)
        data_id = get_param(request,'data_id',None)    
        if data_id != None and data_id != "":
            tranObjs = Topics.objects.filter(id=data_id)
        else:
            tranObjs = Topics.objects.all()
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
        category     = get_param(request, 'category', None)
        sub_category = get_param(request, 'subcategory', None)
        description  = get_param(request,'desc',None)
        category     = cleanstring(category).lower()
        sub_category = cleanstring(sub_category).lower()
        description  = cleanstring(description).lower()
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
    tranObjs = []
    operation = get_param(request, 'operation', "read")
    if operation == "read":
        tranObjs = None
        page_num = get_param(request, 'page_num', None)
        page_size = get_param(request, 'page_size', None)
        data_id = get_param(request,'data_id',None)    
        if data_id != None and data_id != "":
            tranObjs = QuestionFolder.objects.filter(id=data_id)
        else:
            tranObjs = QuestionFolder.objects.all()
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
        folder_name  = get_param(request, 'folder_name', None)
        description  = get_param(request,'desc',None)

        folder_name  = cleanstring(folder_name).lower()
        description  = cleanstring(description).lower()

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

        folder_name  = cleanstring(folder_name).lower()
        description  = cleanstring(description).lower()
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
    operation = get_param(request, 'operation', "read")
    tranObjs = []
    if operation == "read":
        page_num = get_param(request, 'page_num', None)
        page_size = get_param(request, 'page_size', None)
        data_id = get_param(request,'data_id',None)    
        if data_id != None and data_id != "":
            tranObjs = Questions.objects.filter(id=data_id)
        else:
            tranObjs = Questions.objects.all()
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
        question_text           = get_param(request, 'question_text', None)
        question_type           = get_param(request, 'question_type', None)
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
        data_id      = get_param(request, 'data_id', None)
        
        question_text           = get_param(request, 'question_text', None)
        question_type           = get_param(request, 'question_type', None)
        topic_id                = get_param(request, 'topic_id', None)
        total_num_set_answers   = get_param(request, 'num_set', 1)
        difficulty_user         = get_param(request, 'difficulty', None)
        to_evaluate             = get_param(request, 'to_evaluate', True)
        is_passage              = get_param(request, 'is_passage', True)
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



LOCATION_IMAGE = 'questionmgmt/static/image'

if settings.PRODUCTION:
    ADDRESS = 'https://www.ipactesting.com/api/static/'
else:
    ADDRESS = 'http://127.0.0.1:8000/static/'
import uuid

def upload_file(request):
    obj = {}
    obj['status'] = False
    obj['results'] = []
    filetype = get_param(request, 'filetype', None)
    if filetype:
        if filetype=='image':
            if request.method == "POST" and 'file' in request.FILES.keys():
                obj['status'] = True
                for afile in request.FILES.getlist('file'):
                    filename = str(uuid.uuid4())+".jpg"
                    with open(LOCATION_IMAGE+filename, 'wb+') as destination:
                        for chunk in afile.chunks():
                            destination.write(chunk)
                    obj['results'].append(dict(url=ADDRESS+filename))
                obj['counter'] = len(obj['results'])
                obj['msg'] = "Success"
                return HttpResponse(json.dumps(obj,default=json_util.default), content_type='application/json')
        elif filetype=='video':
            if request.method == "POST" and 'file' in request.FILES.keys():
                obj['status'] = True
                afile = request.FILES['file']
                filename = str(uuid.uuid4())+".mp4"
                with open(LOCATION_IMAGE+filename, 'wb+') as destination:
                    for chunk in afile.chunks():
                        destination.write(chunk)
                    obj['results'].append(dict(url=ADDRESS+filename))
                obj['counter'] = len(obj['results'])
                obj['msg'] = "Success"
                return HttpResponse(json.dumps(obj,default=json_util.default), content_type='application/json')
    else:
        return HttpResponseBadRequest("Bad Request")
