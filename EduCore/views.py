from django.shortcuts import render
import json

from django.http import JsonResponse
from EduAdmin.models import UserRole,Dropdown,Mapping,Subjects,User


def sidebar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
             check_user = UserRole.objects.filter(user = request.user.id).first()
             leftpanel = []
             child=[]
             if check_user:
                pannels = Dropdown.objects.filter(pannel=1,deleted_status=False, role = check_user.role).values('id')
                if not pannels or pannels is None:
                    return JsonResponse({'message':'Missing Required Field or Key'},status=400)
                for i in pannels:
                    child_data = list(Dropdown.objects.filter(relation_id = i.get('id'),deleted_status=False).values('name','state'))
                    child.append(child_data)
                master_configuration = Dropdown.objects.filter(pannel=1,deleted_status=False).values('pk','name','icon','type','state')
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


def parents(request):
    if request.method == 'GET':
        data=Dropdown.objects.filter(deleted_status=False).values('id','name')
        if data is None:
            return JsonResponse({'message':'Courses Not Found'},status=204)
        else:
            return JsonResponse(list(data),safe=False)
            
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)

def childs(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if UserRole.objects.filter(role_id='1').exists():
                parent_id=request.GET.get('parent_id')
                data=Dropdown.objects.filter(relation=parent_id,deleted_status=False).values('id','name')
                if data is None:
                    return JsonResponse({'message':'Courses Not Found'},status=204)
                else:
                    return JsonResponse(list(data),safe=False)
            else:
                return JsonResponse({'message':'You Are Not Admin'},status=403)
        else:
            return JsonResponse({'message':'You are not authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)
    
def courses(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if UserRole.objects.filter(role_id='1').exists():
                data=Dropdown.objects.filter(relation='2',deleted_status=False).values('id','name')
                if data is None:
                    return JsonResponse({'message':'Courses Not Found'},status=204)
                else:
                    return JsonResponse(list(data),safe=False)
            else:
                return JsonResponse({'message':'You Are Not Admin'},status=403)
        else:
            return JsonResponse({'message':'You are not authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)


def departments(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if UserRole.objects.filter(role_id='1').exists():
                course_id=request.GET.get('course_id')
                data=Mapping.objects.filter(course=course_id,deleted_status=False).values('department__name', 'department_id')
                if data is None:
                    return JsonResponse({'message':'Courses Not Found'},status=204)
                else:
                    return JsonResponse(list(data),safe=False)
            else:
                return JsonResponse({'message':'You Are Not Admin'},status=403)
        else:
            return JsonResponse({'message':'You are not authenticated'},status=401)
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
        course_id=request.GET.get('course_id')
        department_id=request.GET.get('department_id')
        year=request.GET.get('year')
        subjects=Subjects.objects.filter(department=department_id,year=year,course=course_id,deleted_status=False).values('id','subject_name')
        if subjects:
            return JsonResponse(list(subjects),safe=False)
        else:
            return JsonResponse({'message':'Subject Not avialable'},status=204)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)

def gender(request):
    if request.method == 'GET':
       gender = Dropdown.objects.filter(relation_id = '44',deleted_status=False).values('id','name')
       if gender:
           gender_data = list(gender)
           
           return JsonResponse(gender_data, safe=False)
       else:
           return JsonResponse({'message':'data not found'})
    else:
        return JsonResponse({'message':'invalid request method'})

def title(request):
    if request.method == 'GET':
       title = Dropdown.objects.filter(relation_id = '48',deleted_status=False).values('id','name')
       if title:
           title_data = list(title)
           
           return JsonResponse(title_data, safe=False)
       else:
           return JsonResponse({'message':'data not found'})
    else:
        return JsonResponse({'message':'invalid request method'})

def religion(request):
    if request.method == 'GET':
       religion = Dropdown.objects.filter(relation_id = '40',deleted_status=False).values('id','name')
       if religion:
           religion_data = list(religion)
           
           return JsonResponse(religion_data, safe=False)
       else:
           return JsonResponse({'message':'data not found'})
    else:
         return JsonResponse({'message':'invalid request method'})
    
    