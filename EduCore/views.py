from django.shortcuts import render

import json
from django.http import JsonResponse,HttpResponse
from EduAdmin.models import UserRole,Dropdown,Mapping,User,Roles,Faculty
from datetime import datetime,date
from .models import Subject
from EduCore.models import Subject,SubjectMapping,SubjectTeacherMapping

def logged_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_data=UserRole.objects.get(user=request.user.id)
            username=User.objects.get(pk=user_data.user_id)
            if user_data and username:
                return JsonResponse({'role_id':user_data.role_id,'username':username.username})
            else:
                return JsonResponse({'message':'No content'},status=204)
        else:
            return JsonResponse({'message':'You are not Authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)


def get_parents(request):
    if request.method == 'GET':
        data=Dropdown.objects.filter(deleted_status=False,child__gt=0,pannel=0).values('id','name','child')
        if data is None:
            return JsonResponse({'message':'Courses Not Found'},status=204)
        else:
            return JsonResponse(list(data),safe=False)
            
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)

def parents(request):
    if request.user.is_authenticated:
        id=Roles.objects.get(role_name='Admin',deleted_status=False)
        check_admin=UserRole.objects.filter(user=request.user.id,role_id = id.pk,deleted_status=False).first()
        if check_admin:
            if request.method=='POST':
                load = json.loads(request.body)
                name = load.get('name')
                child = load.get('child')
                parent, created = Dropdown.objects.get_or_create(
                    name=name,
                    added_by=check_admin.user,
                    defaults={'child':child,'can_delete':False,'can_update':True}
                )
                if created:
                    return JsonResponse({'message':'parent created successfully'},status=201)
                else:
                    return JsonResponse({'message':'This parent already exist'},status=409)
            else:
                return JsonResponse({'message':'invalid request method'},status=405)
        else:
            return JsonResponse({'message':'You are not autherised'},status=403)
    else:
        return JsonResponse({'message':'You not authenticated'},status=401)
            
            

def get_childs(request):
    if request.method == 'GET':
        parent_id=request.GET.get('parent_id')
        data=Dropdown.objects.filter(relation=parent_id,deleted_status=False).values('id','name')
        if data is None:
            return JsonResponse({'message':'Courses Not Found'},status=204)
        else:
            return JsonResponse(list(data),safe=False)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)
    
def courses(request):
    if request.method == 'GET':
        id=Dropdown.objects.get(deleted_status=False,name='Courses')
        data=Dropdown.objects.filter(relation=id.relation,deleted_status=False).values('id','name')
        if data is None:
            return JsonResponse({'message':'Courses Not Found'},status=204)
        else:
            return JsonResponse(list(data),safe=False)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)


def departments(request):
    if request.method == 'GET':
        id = request.GET.get('course_id')
        data=Mapping.objects.filter(deleted_status=False, course=id).values('department__name')
        if data is None:
            return JsonResponse({'message':'Courses Not Found'},status=204)
        else:
            return JsonResponse(list(data),safe=False)
           
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)


def years(request):
    if request.method == 'GET':
        course_id=request.GET.get('course_id')
        data=Dropdown.objects.get(pk=course_id,deleted_status=False)
        years=[]
        for i in range(1,data.year+1):
            years.append(i)
        return JsonResponse(years,safe=False)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)


def subjects(request):
    if request.method == 'GET':
        # course_id=request.GET.get('course_id')
        # department_id=request.GET.get('department_id')
        # year=request.GET.get('year')
        subjects=Subject.objects.filter(deleted_status=False).values('id','subject_name','subject_code')
        if subjects:
            return JsonResponse(list(subjects),safe=False)
        else:
            return JsonResponse({'message':'Subject Not avialable'},status=204)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)

def gender(request):
    if request.method == 'GET':
       id=Dropdown.objects.get(deleted_status=False,name='Gender')
       gender = Dropdown.objects.filter(relation_id = id.relation,deleted_status=False).values('id','name')
       if gender:
           gender_data = list(gender)
           
           return JsonResponse(gender_data, safe=False)
       else:
           return JsonResponse({'message':'data not found'},status=204)
    else:
        return JsonResponse({'message':'invalid request method'},status=405)

def title(request):
    if request.method == 'GET':
       id=Dropdown.objects.get(deleted_status=False,name='Title')
       title = Dropdown.objects.filter(relation_id = id.relation,deleted_status=False).values('id','name')
       if title:
           title_data = list(title)
           
           return JsonResponse(title_data, safe=False)
       else:
           return JsonResponse({'message':'data not found'},status=204)
    else:
        return JsonResponse({'message':'invalid request method'},status=405)

def religion(request):
    if request.method == 'GET':
       id=Dropdown.objects.get(deleted_status=False,name='Religion')
       religion = Dropdown.objects.filter(relation_id = id.relation,deleted_status=False).values('id','name')
       if religion:
           religion_data = list(religion)
           
           return JsonResponse(religion_data, safe=False)
       else:
           return JsonResponse({'message':'data not found'},status=204)
    else:
         return JsonResponse({'message':'invalid request method'},status=405)
     
def sidebar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
             check_admin = UserRole.objects.filter(user =request.user.id).first()
             leftpanel = []
             child=[]
             if check_admin:
                pannels = Dropdown.objects.filter(pannel=1,deleted_status=False, role = check_admin.role.id).values('id')
                if not pannels or pannels is None:
                    return JsonResponse({'message':'Missing Required Field or Key'},status=400)
                for i in pannels:
                    child_data = list(Dropdown.objects.filter(relation_id = i.get('id'),deleted_status=False,role = check_admin.role.id).values('name','state'))
                    child.append(child_data)
                master_configuration = Dropdown.objects.filter(pannel=1,deleted_status=False,role=check_admin.role.id).values('pk','name','icon','type','state')
                master_configuration_list = list(master_configuration)
                for i in range(0, len(master_configuration_list)):
                    master_configuration_list[i]['child'] = child[i]
                    leftpanel.append(master_configuration_list[i])
                return JsonResponse(list(leftpanel), safe=False)
             else:
                 return JsonResponse({'message':'User is not Admin'},status=403)         
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'invalid request method'},status=405)
def subject(request):
    if request.method =='POST':
        data = json.loads(request.body)
        if request.user.is_authenticated:
            id=Roles.objects.get(role_name='Admin',deleted_status=False)
            check_admin=UserRole.objects.filter(user=request.user.id,role_id = id.pk,deleted_status=False).first()
            if check_admin:
                subject_name = data.get('subject_name')
                subject_code = data.get('subject_code')   
                if not subject_name or not subject_code:
                    return JsonResponse({'message':'missing required field'},status=400)   
                if subject_code is None or subject_name is None :
                    return JsonResponse({'message':'missing any key'},status=400)
                subjects , created = Subject.objects.get_or_create(
                subject_name= subject_name,
                subject_code=subject_code,
                added_by=check_admin.user
                
                ) 
                if created:
                   return JsonResponse({'message':'subject added successfully'},status=201)
                else:
                   return JsonResponse({'message':'subject already exist'}, status = 409)
            else:
                return JsonResponse({'message':'user is not admin'}, status=403)
        else:
            return JsonResponse({'message':'user is not authenticated'}, status=401)
    else:
        return JsonResponse({'message':'invalid request method'},status = 405)
def subject_mapping(request):
    if request.method=='POST':
        data = json.loads(request.body)
        if request.user.is_authenticated:
            id=Roles.objects.get(role_name='Admin',deleted_status=False)
            check_admin=UserRole.objects.filter(user=request.user.id,role_id = id.pk,deleted_status=False).first()
            if check_admin:
                subject = data.get('subject_id')
                department = data.get('department_id')
                year = data.get('year')
                if not subject or not department or not year:
                    return JsonResponse({'message':'missing required field'},status=400)   
                if subject is None or department is None or year is None:
                    return JsonResponse({'message':'missing any key'},status=400)
                subject_exist = Subject.objects.filter(id = subject).first()
                if subject_exist is None:
                    return JsonResponse({'message':'subject is not found'},status=204)
                department_exist = Mapping.objects.filter(department = department).first()
                if department_exist is None:
                    return JsonResponse({'message':'department not found'},status=204)
                subject_mapping, created=SubjectMapping.objects.get_or_create(
                    subject=subject_exist,
                    department=department_exist,
                    year=year,
                    added_by=check_admin.user
                )
                if created:
                    return JsonResponse({'message':'subject mapping successfully done'})
                else:
                    return JsonResponse({'message':'mapping already exist'},status=409)
            else:
                    return JsonResponse({'messgae':'user is not admin'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'invalid request method'},status=405)
def subject_teacher_mapping(request):
    if request.method=='POST':
        data = json.loads(request.body)
        if request.user.is_authenticated:
            id=Roles.objects.get(role_name='Admin',deleted_status=False)
            check_admin=UserRole.objects.filter(user=request.user.id,role_id = id.pk,deleted_status=False).first()
            if check_admin:
                sub_mapping = data.get('sub_mapping')
                faculty = data.get('faculty')
                if not sub_mapping or not faculty:
                    return JsonResponse({'message':'missing required field'},status=400)   
                if sub_mapping is None or faculty is None :
                    return JsonResponse({'message':'missing any key'},status=400)
                sub_mapping_exist = SubjectMapping.objects.filter(id = sub_mapping).first()
                if sub_mapping_exist is None:
                    return JsonResponse({'message':'mapping is not found'}, status =204)
                faculty_exist = Faculty.objects.filter(id = faculty).first()
                if faculty_exist is None:
                    return JsonResponse({'message':'faculty not found'},status=204)
                teacher_mapping, created = SubjectTeacherMapping.objects.get_or_create(
                faculty=faculty_exist,
                subject=sub_mapping_exist,
                added_by = check_admin.user
                )
                if created:
                    return JsonResponse({'message':'mapping done successfully'})
                else:
                    return JsonResponse({'message':'mapping already exist'},status=409)
            else:
                return JsonResponse({'message':'user is not admin'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'invalid request method'},status=405)
def dropdown_option(request,dropdown):
    if request.method =='GET':
        if dropdown =='gender':
            name = 'Gender'
            return dropdown_value(name)
        elif dropdown =='title':
            name = 'Title'
            return dropdown_value(name)
        elif dropdown =='courses':
            name = 'Courses'
            return dropdown_value(name)
        elif dropdown =='religion':
            name = 'Religion'
            return dropdown_value(name)
        elif dropdown =='select_mapping':
            name = 'Mapping'
            return dropdown_value(name)
    else:
        return JsonResponse({'message':'invalid request method'})
def dropdown_value(name):
         id=Dropdown.objects.filter(deleted_status=False,name=name,pannel=0).first() 
         mapping = Dropdown.objects.filter(relation_id = id.pk,deleted_status=False).values('id','name')
         if mapping:
                 mapping_data = list(mapping)
                 return JsonResponse(mapping_data, safe=False)
         else:
                 return JsonResponse({'messgae':'gender is not found'})
                
                
            
            


    
    