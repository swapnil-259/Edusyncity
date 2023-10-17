from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import json
import re
from .models import User,Roles, UserRole, Faculty,Dropdown,Mapping, Student
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password



def register_faculty(request):
    if request.method == 'POST':
        load= json.loads(request.body)
        first_name = load.get('firstname')
        last_name = load.get('lastname')
        user_name =  load.get('username')
        email =  load.get('email')
        gender =  load.get('gender')
        phone =  load.get('phone')
        age =  load.get('age')
        address =  load.get('address')
        department =  load.get('department')
        qualification = load.get('qualification')
        title = load.get('title')
        subject =  load.get('subject')
        course = load.get('course')
      

        if not re.match(r'(/^[A-Za-z]+$/)', qualification):
              return JsonResponse({'message':'Only Charcters are Alowed in Qulification Field'},status=400)
        
        if user_name or first_name or last_name or email or gender or phone or age or address == None:
              return JsonResponse({'message':'all details is mandatory'}, status = 400)
          
        user=  User.objects.create_user(
                 username = user_name,
                 password = "Kiet@123",
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
            title = title,
            course = course
        )
        roles, created = Roles.objects.get_or_create(rolename= 'Faculty')

        if not created:
            return JsonResponse({'message':'You Already Have This Role'},status=409)
        else:
            UserRole.objects.create(
            user_id = user.id,
            role_id = roles.id,
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

def forgot_password(request):
    if request.method == 'POST':
        load_data=json.loads(request.body)
        username = load_data.get('username')
        old_password = load_data.get('old_password')
        new_password = load_data.get('new_password')
        user =  authenticate(username= username, password = old_password)
        if user is not None:
            User.objects.filter(id = request.user.id).update(password = make_password(new_password))
            return JsonResponse({'message':'Password Updated Successfully'},status=200)
        else:
            return JsonResponse({'message':'Your Old Password Does Not Matched'},status=401)
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
        
        if request.user.is_authenticated:
            course_data = json.loads(request.body)
            course_name = course_data.get('course_name')
            if course_name is None or not course_name:
                return JsonResponse({'message':'Missing Required Filed or Key'},status=400)
            check_admin = UserRole.objects.filter(role_id = '1').first()
            user_exist = User.objects.get(pk = request.user.id)
            course_id = Dropdown.objects.get(name='Courses').pk
            if not course_id:
                return JsonResponse({'message':'You have no attribute named cources'},status=400)
            if check_admin: 
                
                course_exist , created = Dropdown.objects.get_or_create(
                    name = course_name,
                    relation_id = course_id,
                    added_by = user_exist,
                    can_update = True,
                    type = type
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
                    departement_data=json.loads(request.body)
                    course_id = departement_data.get('id')
                    name=departement_data.get('name')
                    state = departement_data.get('state')
                    type = departement_data.get('type')
                    course_exist= Dropdown.objects.filter(pk = course_id).first()
                    print(course_exist.child)
                    if course_exist:    
                        dept , created =Dropdown.objects.get_or_create(name=name,relation=course_exist,can_delete=False,can_update=True,added_by=user_exist, state=state, type = type)
                        print(dept.child)
                        if created:
                            childs=course_exist.child
                            childs=int(childs)-1
                            course_exist.child= childs
                            course_exist.save()
                       
                            return JsonResponse({'message':'Department added Successfully'},status=201)
                        else:
                            return JsonResponse({'message':'Department already exist'},status=409)

                    else:
                        return JsonResponse({'message':'Attribute Courses Does Not Exists'},status=204)
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
                            return JsonResponse({'message':'successfully department added to course'},status=201)
                        else:
                            return JsonResponse({'message':'departemnt already assigned to this course'},status=409)
                    else:
                        return JsonResponse({'message':'course/departemnt not exist'},status=204)
            else:
                return JsonResponse({'message':'user is not Admin'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'invalid request method'},status=405)
    

def register_student(request):
    if request.method == 'POST':
        load=json.loads(request.body)
        first_name = load.get('firstname')
        last_name = load.get('lastname')
        user_name =  load.get('username')
        father_name = load.get('father_name')
        mother_name = load.get('mother_name')
        email =  load.get('email')
        gender =  load.get('gender')
        contact =  load.get('contact')
        age =  load.get('age')
        address =  load.get('address')
        course =  load.get('course')
        department = load.get('department')
        year = load.get('year')
        
        user = User.objects.create_user(
            first_name= first_name,
            last_name=last_name,
            username = user_name,
            email=email,
            password = "Kiet@123"
        )
        Student.objects.create(
            user = user.id,
            department = department,
            age = age,
            gender = gender,
            address= address,
            year = year,
            contact= contact,
            course = course,
            father_name = father_name,
            mother_name= mother_name
        )
        roles, created = Roles.objects.get_or_create(rolename= 'Student')

        if not created:
            return JsonResponse({'message':'You Already Have This Role'},status=409)
        else:
            UserRole.objects.create(
            user_id = user.id,
            role_id = roles.id,
            )
            return JsonResponse({'message':'Registration Succesfull'},status=201)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)

def dropdown(request):
    if request.method == 'POST':
        load = json.loads(request.body)
        if request.user.is_authenticated:
            check_admin = UserRole.objects.filter(role_id = '1').exists()
            if check_admin:
                id = load.get('id')
                name = load.get('name')
                parent=Dropdown.objects.filter(id = id, child__gte=0).first()
                if parent is not None:
                    dropdown, created=Dropdown.objects.get_or_create(
                        name= name,
                        added_by=check_admin.user,
                        relation_id = parent.id,
                        child = parent.child -1,
                    )
                    if created:
                        return JsonResponse({'message':'dropdown added successfully'},status=201)
                    else:
                        return JsonResponse({'message':'dropdown already exist'},status=409)
                else:
                    return JsonResponse({'message':'You can not add child for this Parent'},status=409)
                
            else:
                return JsonResponse({'message':'user is not admin'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Reqest Method'},status=405)
        
                
                
                        
            
            

        
        





