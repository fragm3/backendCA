from django.shortcuts import render
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
import operator

# Slack Integration Check


# Create your views here.
def crud_testfolders(request):
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
        if data_id != None and data_id != "":
            tranObjs = TestFolder.objects.filter(id=data_id)
        else:
            tranObjs = TestFolder.objects.all().order_by('folder_name')
            # Filters/Sorting Start
            if search !=None and search !="":
                tranObjs = tranObjs.filter(Q(folder_name__icontains=search) | Q(description__icontains=search))
            
            if sort_by !=None and sort_by !="":
                tranObjs = tranObjs.order_by(sort_by)
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



    if operation == "create":
        folder_name  = get_param(request, 'folder_name', None)
        description  = get_param(request,'desc',None)
        folder_name  = cleanstring(folder_name)
        description  = cleanstring(description)
        tranObjs     = TestFolder.objects.filter(folder_name=folder_name)

        if len(tranObjs):
            obj['message'] = "Folder Already Exists!"
        else:
            folder = TestFolder.objects.create(folder_name=folder_name,description=description)
            tranObjs = [folder]
            obj['message'] = "Folder Created"

    if operation == "update":
        data_id      = get_param(request, 'data_id', None)
        folder_name  = get_param(request, 'folder_name', None)
        description  = get_param(request,'desc',None)

        folder_name  = cleanstring(folder_name)
        description  = cleanstring(description)
        try:
            folder = TestFolder.objects.get(id=data_id)
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
            folder  = TestFolder.objects.get(id=data_id)
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
