from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import json
import re
from .models import User,Roles, UserRole, Faculty,Dropdown,Mapping 
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
            user_exist = User.objects.get(pk = request.user.id)
            print(user_exist.id)
            if check_admin: 
              role_exist , created= Roles.objects.get_or_create(
                role_name = name,
                added_by = user_exist
              )
              if created:
               return JsonResponse({'message':'role successfully added'},status=201)
              else:
                  return JsonResponse({'message':'role already exist'},status=409)
            else:
                return JsonResponse({'message':'user is not admin'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated '},status=401)
        
    if request.method == "PUT":
        load = json.loads(request.body)
        new_name=load.get('new_name')
        role_id=load.get('role_id')
        if new_name is None or role_id is None or not new_name or not role_id:
            return JsonResponse({'message':'Missing Required Filed or Key'},status=400)
        if request.user.is_authenticated:
            check_admin = UserRole.objects.filter(role_id = '1').first()
            user_exist = User.objects.get(pk = request.user.id)
            print(user_exist.id)
            if check_admin:
                Roles.objects.filter(pk=role_id).update(name=new_name)
                return JsonResponse({'message':'Role Updated Successfully'},status=200)
            else:
                return JsonResponse({'message':'user is not admin'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated '},status=401)


    else:
        return JsonResponse({'message':'invalid request method'},status=405)


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
            user_exist = User.objects.get(pk = request.user.id)
            if UserRole.objects.filter(user=request.user.id,role_id = '1').first():
                    load=json.loads(request.body)
                    course_id = load.get('id')
                    name=load.get('name')
                    course_exist= Dropdown.objects.filter(pk = course_id).first()
                    print(course_exist.child)
                    if course_exist:    
                     dept , created =Dropdown.objects.get_or_create(name=name,relation=course_exist,can_delete=False,can_update=True,added_by=user_exist)
                     print(dept.child)
                     if created:
                        childs=course_exist.child
                        childs=int(childs)-1
                        course_exist.child= childs
                        course_exist.save()
                       
                        return JsonResponse({'message':'Department added Successfully'},status=409)
                     else:
                        return JsonResponse({'message':'Department already exist'},status=201)
            else:
                return JsonResponse({'message': 'You Are Not Authorised'},status=403)   
        else:
            return JsonResponse({'message': 'User not logged in'},status=401) 
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)   
    
    
      
def assign_department_to_course(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user_exist = User.objects.get(pk = request.user.id)
            if UserRole.objects.filter(user=request.user.id,role_id = '1').first():
                    load=json.loads(request.body)
                    course_id = load.get('course_id')
                    department_id = load.get('department_id')
                    mapping, created = Mapping.objects.get_or_create(course= course_id, department = department_id, added_by = user_exist )
                    if created:
                        course_exist= Dropdown.objects.filter(pk = course_id).first()
                        department_exist = Dropdown.objects.filter(pk = department_id).first()
                    if course_exist is not None and department_exist is not None:
                        mapping, created = Mapping.objects.get_or_create(course= course_exist, department = department_exist, added_by = user_exist )
                        if created:
                            return JsonResponse({'message':'successfully department added to course'})
                        else:
                            return JsonResponse({'message':'departemnt already assigned to this course'})
                    else:
                        return JsonResponse({'message':'course/departemnt not exist'})
            else:
                return JsonResponse({'message':'user is not Admin'})
        else:
            return JsonResponse({'message':'user is not authenticated'})
    else:
        return JsonResponse({'message':'invalid request method'})
            