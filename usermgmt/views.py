from django.shortcuts import render
from overall.views import cleanstring,get_param,random_str_generator
from django.http import HttpResponseRedirect,HttpResponseForbidden,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from models import CAUsers
from mailing import views as mailing
import math
import json

# Create your views here.
# Creating or checking a users existence in the database
def crud_user(request):
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
            tranObjs = CAUsers.objects.filter(id=search_id)
        else:
            tranObjs = CAUsers.objects.all()
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

        fname            = get_param(request, 'fname', None)
        lname            = get_param(request, 'lname', None)
        email            = get_param(request, 'email', None)
        is_admin         = get_param(request, 'is_admin', "0")
        is_manager       = get_param(request, 'is_manager', "0")
        is_staff         = get_param(request, 'is_staff', "0")

        email = email.lower()
        email = cleanstring(email)
        fname  = fname.lower()
        lname  = lname.lower()
        fname  = cleanstring(fname)
        lname  = cleanstring(lname)
        users = CAUsers.objects.filter(email=email)

        if len(users):
            obj['message'] = "User Already Exists!"
        else:
            user  = create_check_user(firstname=fname, lastname = lname, email=email)
            if is_admin:
                if is_admin == "1":
                    user.is_admin = True
                    user.is_manager = True
                    user.is_staff = True
                else:
                    user.is_admin = False
                    if is_manager:
                        if is_manager == "1":
                            user.is_manager = True
                            user.is_staff = True
                        else:
                            user.is_manager = False
                            if is_staff:
                                if is_staff == "1":
                                    user.is_staff = True
                                else:
                                    user.is_staff = False

            user.save()
            tranObjs = [user]
            obj['message'] = "User Created"

    if operation == "update":
        data_id          = get_param(request, 'data_id', None)
        fname            = get_param(request, 'fname', None)
        lname            = get_param(request, 'lname', None)
        is_admin         = get_param(request, 'is_admin', "0")
        is_manager       = get_param(request, 'is_manager', "0")
        is_staff         = get_param(request, 'is_staff', "0")
        is_activate      = get_param(request,'is_active',"1")
        fname  = fname.lower()
        lname  = lname.lower()
        fname  = cleanstring(fname)
        lname  = cleanstring(lname)

        try:
            user = CAUsers.objects.get(id=data_id)
        except:
            user = None
        obj['message'] = "User Not Found"

        if user:
            if is_activate:
                if is_activate == "0":
                    user.active = False
                else:
                    user.active = True

            user.first_name = fname
            user.last_name  = lname
            if is_admin:
                if is_admin == "1":
                    user.is_admin = True
                    user.is_manager = True
                    user.is_staff = True
                else:
                    user.is_admin = False
                    if is_manager:
                        if is_manager == "1":
                            user.is_manager = True
                            user.is_staff = True
                        else:
                            user.is_manager = False
                            if is_staff:
                                if is_staff == "1":
                                    user.is_staff = True
                                else:
                                    user.is_staff = False
            user.save()
            tranObjs = [user]
            obj['message'] = "User Updated"

    if operation == "delete":
        data_id      = get_param(request, 'data_id', None)
        try:
            user  = CAUsers.objects.get(id=data_id)
        except:
            user = None
        obj['message'] = "User Not Found"

        # Code Correction Required Later after checking links
        if user:
            user.active = False
            user.save()
            obj['message'] = "User Deleted"

    for trans in tranObjs:
        obj['result'].append({
        'id':trans.id,
        'first_name':trans.first_name,
        'last_name':trans.last_name,
        'is_admin':trans.is_admin,
        'email':trans.email,
        'is_manager':trans.is_manager,
        'is_staff':trans.is_staff,
        'secret_string':trans.secret_string,
        'auth_token':trans.auth_token,
        'is_active':trans.active
    })
    obj['status'] = True
    return HttpResponse(json.dumps(obj), content_type='application/json')


def create_check_user(firstname,lastname,email):
    if email:
        users = CAUsers.objects.filter(email=email)
        if len(users):
            user_old = users[0]
            user_old.active = True
            user_old.save()
            return user_old
        else:
            user_new = CAUsers.objects.create(first_name=firstname,last_name=lastname,email=email)
            user_new.set_password("careerannafirstlogin")
            user_new.secret_string = (user_new.id + random_str_generator())
            user_new.auth_token = (user_new.id + random_str_generator())
            user_new.save()
            return user_new

# logging in with password
def login_view_staff(request):
    obj = {}
    obj['status'] = False
    email           = get_param(request, 'email', None)
    password        = get_param(request, 'pass', None)
    secret_string   = get_param(request, 'sec_string', None)
    auth_token      = get_param(request, 'auth_token', None)
    print auth_token
    if email:
        email = email.lower()
        email = cleanstring(email)
    obj['result'] = {}
    obj['user'] = {}
    message = ""
    if auth_token:
        try:
            user = CAUsers.objects.get(auth_token=auth_token,active=True)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            message = "User Found"
            login(request, user)
            obj['user']['auth_token'] = auth_token
            obj['user']['id'] = user.id
            obj['user']['first_name'] = user.first_name
            obj['user']['last_name'] = user.last_name
            obj['user']['email'] = user.email
            obj['user']['is_admin'] = user.is_admin
            obj['user']['is_manager'] = user.is_manager
            obj['user']['is_staff'] = user.is_staff
            obj['result']['auth'] = True
            message = "Login Success!"
            print 1
        except:
            obj['result']['auth'] = False
            message = "Auth Token Expired"
            obj['user'] = None
            print 2
    else:
        try:
            user = CAUsers.objects.get(email=email,active=True)
            if user:
                print 3
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                message = "User Found"
                if user.check_password(password):
                    print 4
                    login(request, user)
                    new_string = user.id + random_str_generator()
                    user.auth_token = new_string
                    obj['user']['auth_token'] = new_string
                    obj['user']['id'] = user.id
                    obj['user']['first_name'] = user.first_name
                    obj['user']['last_name'] = user.last_name
                    obj['user']['email'] = user.email
                    obj['user']['is_admin'] = user.is_admin
                    obj['user']['is_manager'] = user.is_manager
                    obj['user']['is_staff'] = user.is_staff
                    obj['result']['auth'] = True
                    message = "Login Success!"
                    user.save()
                elif user.secret_string == secret_string:
                    print 5
                    login(request, user)
                    new_string = user.id + random_str_generator()
                    user.auth_token = new_string
                    obj['user']['auth_token'] = new_string
                    obj['user']['id'] = user.id
                    obj['user']['first_name'] = user.first_name
                    obj['user']['last_name'] = user.last_name
                    obj['user']['email'] = user.email
                    obj['user']['is_admin'] = user.is_admin
                    obj['user']['is_manager'] = user.is_manager
                    obj['user']['is_staff'] = user.is_staff
                    obj['result']['auth'] = True
                    message = "Login Success!"
                    user.save()
                else:
                    print 6
                    message = "Incorrect Password"
                    obj['result']['auth'] = False
            else:
                print 7
                message = "User Doesn't exist"
                obj['result']['auth'] = False
                obj['user'] = None
        except CAUsers.DoesNotExist:
            print 8
            if email:
                print 9
                message = "User Doesn't exist"
            obj['result']['auth'] = False
            obj['user'] = None
    obj['status'] = True
    obj['message'] = message
    response = HttpResponse(json.dumps(obj), content_type='application/json')
    return response

def send_password_reset(request):
    obj = {}
    obj['status'] = False
    email = get_param(request, 'email', None)
    randstring = ""
    try:
        user = CAUsers.objects.get(email=email,active=True)
        if user:
                print 1
                randstring = user.id + random_str_generator(size=6)
                # Mailing function to send email to the user
                message = "Reset Request Success"
                user.secret_string = randstring
                user.save()
                mailing.send_password_reset_email(name=user.first_name, email=user.email, secret_string=randstring.encode('utf-8'))
        else:
            message = "User Doesn't exist"
    except CAUsers.DoesNotExist:
        message = "User Doesn't exist"
        obj['user'] = None
    obj['status'] = True
    obj['message'] = message
    response = HttpResponse(json.dumps(obj), content_type='application/json')
    return response

def reset_pass_staff(request):
    obj = {}
    obj['status'] = False
    password        = get_param(request, 'pass', None)
    secret_string   = get_param(request, 'sec_string', None)
    try:
        user = CAUsers.objects.get(secret_string=secret_string,active=True)
        user.set_password(password)
        randstring = user.id + random_str_generator(size=6)
        randstring2 = user.id + random_str_generator(size=6)
        user.secret_string = randstring
        user.auth_token = randstring2
        user.save()
        obj['message'] = "Password Reset Success"
    except:
        obj['message'] = "Invalid Request Please Try Resetting the Password Again"
    obj['status'] = True
    
    return HttpResponse(json.dumps(obj), content_type='application/json')
# logging out

def logout_view_staff(request):
    obj = {}
    obj['status'] = False
    user = request.user
    user.auth_token = user.id + random_str_generator()
    user.save()
    logout(request)
    obj['result'] = "Logout Success"
    obj['status'] = True
    
    response = HttpResponse(json.dumps(obj), content_type='application/json')
    return response



# <------------------ End ------------------------->