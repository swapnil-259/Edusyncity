from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import json
import re
from .models import User,Roles, UserRole, Faculty,Dropdown
from django.contrib.auth import authenticate,login,logout
from django.db.models.functions import Lower


def register_faculty(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        user_name =  request.POST.get('username')
        email =  request.POST.get('email')
        gender =  request.POST.get('gender')
        phone =  request.POST.get('phone')
        age =  request.POST.get('age')
        address =  request.POST.get('address')
        department =  request.POST.get('department')
        qualification = request.POST.get('qualification')
        subject =  request.POST.get('subject')
        profile_pic = request.FILES.get('profilepic')
        password =  request.POST.get('password')
        confirm_pass =  request.POST.get('confirmpassword')

        if not re.match(r'(/^[A-Za-z]+$/)', qualification):
              return JsonResponse({'message':'Only Charcters are Alowed in Qulification Field'},status=400)
        
        if password != confirm_pass:
              return JsonResponse({'message': 'Password and confirmPassword do not match'}, status=400)
        if user_name or first_name or last_name or email or gender or phone or age or address or password or confirm_pass== None:
              return JsonResponse({'message':'all details is mandatory'}, status = 400)
          
        user=  User.objects.create_user(
                 username = user_name,
                 password = password,
                 first_name=first_name,
                 last_name=last_name,
                 email=email
               ) 
        Faculty.objects.create(
            user_id = user.id,
            department_id = department,
            subject_id = subject,
            qualification = qualification,
            address = address,
            profile_picture = profile_pic   
        )
        roles, created = Roles.objects.get_or_create(rolename= 'Faculty')

        if not created:
            return JsonResponse({'message':'You Already Have This Role'},status=409)
        else:
            UserRole.objects.create(
            user_id = user.id,
            role_id = roles.id,
            department = department
            )
            return JsonResponse({'message':'Registration Succesfull'},status=201)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)


def login_user(request):
    
    if request.method == 'POST':

        load=json.loads(request.body)
        user_name = load.get('username')
        password = load.get('password')
       
        if user_name is None or password is None:
            return JsonResponse({'message': 'Missing any Key.'}, status=400)
        
        if not user_name or not password:
            return JsonResponse({'message': 'Missing Required field.'}, status=400)
        
        user=authenticate(username=user_name,password=password)
        if user is not None:
            login(request,user)
            user_exist = UserRole.objects.filter(user_id = request.user.id).values('role','role__role_name')
            user_data = list(user_exist)
            return JsonResponse(user_data, safe=False)
        else:
            auth= User.objects.get(email=user_name.lower()).username
            user2 = authenticate(username=auth, password= password)
            if user2 is not None:
                login(request, user2)
                user_exist2 = UserRole.objects.filter(user_id = request.user.id).values('role','role__role_name')
                user_data2 = list(user_exist2)
                return JsonResponse(user_data2, safe=False)
            else:
                return JsonResponse({'message':'Incorrect Username/Email Or password'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)

def logout_user(request):      
    if request.method == 'GET':
        
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'message':'Logged Out Succesfully'},status=200)
        else:
            return JsonResponse({'message':'User Is Not Authenticated'},status=401) 
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405) 
    
    
          
def add_role(request):
    
    if request.method =='POST':
        roles_data = json.loads(request.body)
        name=roles_data.get('name')
        if name is None or not name:
            return JsonResponse({'message':'Missing Required Filed or Key'},status=400)
        if request.user.is_authenticated:
            check_admin = UserRole.objects.filter(role_id = '1').first()
            if check_admin: 
              role_exist , created= Roles.objects.get_or_create(
                role_name = name,
              )
              if created:
               return JsonResponse({'message':'role successfully added'})
              else:
                  return JsonResponse({'message':'role already exist'})
            else:
                return JsonResponse({'message':'user is not admin'})
        else:
            return JsonResponse({'message':'user is not authenticated '})
    else:
        return JsonResponse({'message':'invalid request method'})


def add_course(request):
    
    if request.method == 'POST':
        course_data = json.loads(request.body)
        course_name = course_data.get('course_name')
        child_count = course_data.get('child_count')
        if course_name is None or not child_count:
            return JsonResponse({'message':'Missing Required Filed or Key'},status=400)
        if request.user.is_authenticated:
            check_admin = UserRole.objects.filter(role_id = '1').first()
            user_exist = User.objects.get(pk = request.user.id)
            course_id = Dropdown.objects.get(name='Courses').pk
            if not course_id:
                return JsonResponse({'message':'You Have No Attribute Named Cources'},status=400)
            if check_admin: 
                
                course_exist , created = Dropdown.objects.get_or_create(
                    name = course_name,
                    child = child_count,
                    relation_id = course_id,
                    added_by = user_exist,
                    can_update = True
                )
                if created:
                    return JsonResponse({'message':'Course successfully added'},status=201)
                else:
                  return JsonResponse({'message':'Course already exist'},status=409)
            else:
                return JsonResponse({'message':'user is not admin'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated '},status=401)
    else:
        return JsonResponse({'message':'invalid request method'},status=405)   

def add_departments(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if UserRole.objects.filter(user=request.user.id,role_id = '1').exists():
                if Dropdown.objects.filter(pk="course id",child__gt=0):
                    load=json.loads(request.body)
                    name=load.get('name')
                    dept , created =Dropdown.objects.get_or_create(name=name,relation="deptid",can_delete=True,can_edit=True,added_by=request.user.id)
                    if created:
                        return JsonResponse({'message':'Department Already Exists'},status=409)
                    else:
                        childs=dept.child
                        dept.child=childs-1
                        dept.save()
                        return JsonResponse({'message':'Department Added Successfully'},status=201)
            else:
                return JsonResponse({'message': 'You Are Not Autherised'},status=403)   
        else:
            return JsonResponse({'message': 'User not logged in'},status=401) 
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)     
       