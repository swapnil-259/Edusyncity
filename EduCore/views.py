from django.shortcuts import render

from django.http import JsonResponse
from EduAdmin.models import UserRole,Dropdown,Mapping 


def sidebar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
             check_admin = UserRole.objects.filter(role_id = '1').first()
             leftpanel = []
             child=[]
             if check_admin:
                pannels = Dropdown.objects.filter(pannel=1).values('id')
                if not pannels or pannels is None:
                    return JsonResponse({'message':'Missing Required Field or Key'},status=400)
                for i in pannels:
                    child_data = list(Dropdown.objects.filter(relation_id = i.get('id')).values('name','state'))
                    child.append(child_data)
                master_configuration = Dropdown.objects.filter(pannel=1).values('pk','name','icon','type','state')
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
    
def courses(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if UserRole.objects.filter(role_id='1').exists():
                data=Dropdown.objects.filter(relation='2').values('id','name')
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
                data=Mapping.objects.filter(course=course_id).values('id','department__name')
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
        data=Dropdown.objects.get(pk=course_id)
        print(data.year)
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
        data=Dropdown.objects.get(pk=course_id)
        print(data.year)
        years=[]
        for i in range(1,data.year+1):
            years.append(i)
        return JsonResponse(years,safe=False)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)