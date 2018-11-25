from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponseForbidden,HttpResponse
from django.core.paginator import Paginator
from django.core import serializers
from models import *
from overall.views import get_param,cleanstring
import math
import json
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
        search_id = get_param(request,'search_id',None)    
        if search_id != None and search_id != "":
            tranObjs = Topics.objects.filter(id=search_id)
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
        search_id = get_param(request,'search_id',None)    
        if search_id != None and search_id != "":
            tranObjs = QuestionFolder.objects.filter(id=search_id)
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
        search_id = get_param(request,'search_id',None)    
        if search_id != None and search_id != "":
            tranObjs = Passages.objects.filter(id=search_id)
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
        order       = get_param(request, 'order', "1")
        data_dict   = get_param(request, 'data_dict', [])
        if data_dict:
            data_dict = json.loads(data_dict)
        order        = int(order)
        tranObjs     = Passages.objects.filter(header=header,text=text)

        if len(tranObjs):
            obj['message'] = "Passage Already Exists!"
        else:
            passage = Passages.objects.create(header=header,text=text,order=order,data_table=data_dict)
            tranObjs = [passage]
            obj['message'] = "Passage Created"

    if operation == "update":
        data_id      = get_param(request, 'data_id', None)
        header      = get_param(request, 'header', None)
        text        = get_param(request, 'text', None)
        order       = get_param(request, 'order', "1")
        data_dict   = get_param(request, 'data_dict', [])
        if data_dict:
            data_dict = json.loads(data_dict)
        order        = int(order)  
        try:         
            passage = Passages.objects.get(id=data_id)
        except:
            passage = None
        obj['message'] = "Passage Not Found"
        if passage:
            passage.header = header
            passage.text = text
            passage.order = order
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
                    # To Be Checked After Question Addions
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
        'order':trans.order,
        'data_table':trans.data_table
    })
    obj['status'] = True
    return HttpResponse(json.dumps(obj), content_type='application/json')


