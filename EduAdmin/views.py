from django.shortcuts import render
from django.http import JsonResponse
import json
import re
from .models import User,Roles, UserRole, Faculty,Dropdown,Mapping, Student
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from datetime import datetime,date
from django.db.models import Q

def validation(email = None,firstname = None,lastname = None,fathername = None, mothername = None):
     print(email,firstname,lastname)
     if firstname is not None:
         if not re.match(r'^[A-Za-z\s]+$',firstname):
           return JsonResponse({'message':'Invalid firstname format'},status=400)
     if lastname is not None:
      if not re.match(r'^[A-Za-z\s]+$',lastname):
        return JsonResponse({'message':'Invalid lastname format'},status=400)
     if fathername is not None:
      if not re.match(r'^[A-Za-z\s]+$',fathername):
        return JsonResponse({'message':'Invalid fathername format'},status=400)
     if mothername is not None:
      if not re.match(r'^[A-Za-z\s]+$',mothername):
        return JsonResponse({'message':'Invalid mother_name format'},status=400)
     if email is not None:
      if not re.match(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b',email):
        return JsonResponse({'message':'Match Your email Requirements'},status=400)
    
    
def register_faculty(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            id=Roles.objects.get(role_name='Admin',deleted_status=False)
            admin_exist=UserRole.objects.filter(user=request.user.id,role_id = id.pk,deleted_status=False).first()
            if admin_exist:
                load= json.loads(request.body)
                firstname = load.get('firstname')
                lastname = load.get('lastname')
                user_name =  load.get('username')
                email =  load.get('email')
                gender =  load.get('gender')
                contact =  load.get('contact')
                age =  load.get('age')
                address =  load.get('address')
                qualification = load.get('qualification')
                title = load.get('title')
                print(firstname,lastname)
                if age is ' ' or int(age) <= 0:
                    return JsonResponse({'message':'Age Can Not Be Negative or blank space'},status=400)
                if not user_name or not firstname or not lastname or not email or not gender or not contact or not age or not address  or not qualification or not title :
                      return JsonResponse({'message':'Missing Required Field'}, status = 400)
                if user_name is None or email is None or firstname is None or lastname is None or  age is None or gender is None or contact is None or address is None or qualification is None or title is None :
                    return JsonResponse({'messge':'Missing any key'},status=400) 
                if user_name is ' ' or email is ' ' or firstname is ' ' or lastname is ' ' or age is ' ' or gender is ' ' or contact is ' ' or address is ' ':
                    return JsonResponse({'messsage':'You Are Passing Space to the Field'},status=400)
                print(firstname,lastname)
                # if not re.match(r'^[a-zA-Z0-9_@-]{8,15}$',user_name):
                #     return JsonResponse({'message':'Match Your Username Requirements'},status=400)
                validation(email,firstname,lastname)
              
                
                # if not re.match(r'^[A-Za-z\s]+$', first_name):
                #     return JsonResponse({'message':'Invalid first_name format'},status=400)
                # if not re.match(r'^[A-Za-z\s]+$', last_name):
                #     return JsonResponse({'message':'Invalid last_name format'},status=400)
                # if not re.match(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b',email):
                #     return JsonResponse({'message':'Match Your email Requirements'},status=400)
                gender_exist = Dropdown.objects.filter(id = gender ).first()
                if gender_exist is None:
                    return JsonResponse({'message':'Gender Not an instance'},status=400)
                title_exist = Dropdown.objects.filter(id = title).first()
                if title_exist is None:
                    return JsonResponse({'message':'Title Not an Instance'},status=400)
                if User.objects.filter(username=user_name).first():
                    return JsonResponse({'message':'Username Already exists'},status=409)
                elif User.objects.filter(email=email).first():
                    return JsonResponse({'message':'Email Already exists'},status=409)
                
                user=  User.objects.create_user(
                username = user_name,
                password = "Kiet@123",
                first_name=firstname,
                last_name=lastname,
                email=email
                ) 
                Faculty.objects.create(
                user_id = user.id,
                qualification = qualification,
                address = address,
                title = title_exist,
                contact= contact,
                added_by = admin_exist.user,
                age = age,
                gender = gender_exist
                )
                roles, created = Roles.objects.get_or_create(role_name= 'Teacher')
                UserRole.objects.create(
                    user_id = user.id,
                    role_id = roles.id,
                    added_by = admin_exist.user
                    )
            else:
                return JsonResponse({'message':'You are not Admin'},status=403)
        else:
            return JsonResponse({'message':'You are not Authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)


def register_student(request):
    if request.method == 'POST':
         if request.user.is_authenticated:
            id=Roles.objects.get(role_name='Admin',deleted_status=False)
            admin_exist=UserRole.objects.filter(user=request.user.id,role_id = id.pk,deleted_status=False).first()
            if admin_exist:
                load=json.loads(request.body)
                firstname = load.get('first_name')
                lastname = load.get('last_name')
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
                religion = load.get('religion')
                
                if age is ' ' or int(age) <= 0:
                    return JsonResponse({'message':'Age Can Not Be Negative or blank space'},status=400)

                if not user_name or not firstname or not lastname or not email or not gender or not contact or not age or not address or not department or not father_name or not mother_name or not year or not course or not religion:
                              return JsonResponse({'message':'Missing Required Field'}, status = 400)
                if user_name is None or email is None or firstname is None or lastname is None or  age is None or gender is None or contact is None or address is None or father_name is None or mother_name is None or year is None or course is None or religion is None:
                            return JsonResponse({'messge':'Missing any key'},status=400) 
             
                if user_name is ' ' or email is ' ' or firstname is ' ' or lastname is ' ' or age is ' ' or gender is ' ' or contact is ' ' or address is ' ':
                    return JsonResponse({'messsage':'You Are Passing Space to the Field'},status=400)
                # if not re.match(r'^[a-zA-Z0-9_@-]{8,15}$',user_name):
                #     return JsonResponse({'message':'Match Your Username Requirements'},status=400)
                # if not re.match(r'^[A-Za-z\s]+$', first_name):
                #     return JsonResponse({'message':'Invalid first_name format'},status=400)
                # if not re.match(r'^[A-Za-z\s]+$', father_name):
                #     return JsonResponse({'message':'Invalid first_name format'},status=400)
                # if not re.match(r'^[A-Za-z\s]+$', mother_name):
                #     return JsonResponse({'message':'Invalid first_name format'},status=400)
                # if not re.match(r'^[A-Za-z\s]+$', last_name):
                #     return JsonResponse({'message':'Invalid last_name format'},status=400)
                # if not re.match(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b',email):
                #     return JsonResponse({'message':'Match Your email Requirements'},status=400)
                

                gender_exist = Dropdown.objects.filter(id = gender ).first()
                if gender_exist is None:
                    return JsonResponse({'message':'Gender Not an instance'},status=400)
                department_exist = Mapping.objects.filter(department = department).first()
                if department_exist is None:
                    return JsonResponse({'message':'Department Not an Instance'},status=400)
                course_exist = Dropdown.objects.filter(id = course).first()
                if course_exist is None:
                    return JsonResponse({'message':'Course Not an Instance'},status=400)
                religion_exist = Dropdown.objects.filter(id = religion).first()
                if religion_exist is None:
                    return JsonResponse({'message':'Religion Not an Instance'},status=400)
                if User.objects.filter(username=user_name).exists():
                    return JsonResponse({'message':'Username Already exists'},status=409)
                elif User.objects.filter(email=email).exists():
                    return JsonResponse({'message':'Email Already exists'},status=409)


                user = User.objects.create_user(
                    first_name= firstname,
                    last_name=lastname,
                    username = user_name,
                    email=email,
                    password = "Kiet@123"
                )
                Student.objects.create(
                    user_id = user.id,
                    department = department_exist,
                    age = age,
                    gender = gender_exist,
                    address= address,
                    year = year,
                    contact = contact,
                    course = course_exist,
                    father_name = father_name,
                    mother_name= mother_name,
                    religion = religion_exist,
                    added_by = admin_exist.user
                )
                roles, created = Roles.objects.get_or_create(role_name= 'Student')
                UserRole.objects.create(
                    user_id = user.id,
                    role_id = roles.id,
                    added_by = admin_exist.user
                    )
                return JsonResponse({'message':'registration Successful'})
            else:   
                return JsonResponse({'message':'user is not admin'},status=403)
         else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
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
        
        user=User.objects.filter(Q(username=user_name)|Q(email=user_name)).first()

        if user is not None and user.check_password(password):
            login(request,user)
            user_exist = UserRole.objects.filter(user_id = request.user.id).values('role','role__role_name')
            user_data = list(user_exist)
            return JsonResponse(user_data, safe=False)
        else:
            return JsonResponse({'message':'You are not authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)

def change_password(request):
    if request.method == 'POST':
        load_data=json.loads(request.body)
        username = load_data.get('username')
        old_password = load_data.get('old_password')
        new_password = load_data.get('new_password')
        
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$",new_password):
            return JsonResponse({'message':'Match Your Password Requirements'},status=400)
        
        # user =  authenticate(username= username, password = old_password)
        user=User.objects.filter(Q(username=username)|Q(email=username)).first()
        if user is not None and user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return JsonResponse({'message':'Password Updated Successfully'})
        else:
            return JsonResponse({'message':'Incorrect username or password'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)


def logout_user(request):      
    if request.method == 'GET':
        
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'message':'Logged Out Succesfully'})
        else:
            return JsonResponse({'message':'User Is Not Authenticated'},status=401) 
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405) 
    
    
          
def add_role(request):
    
    if request.method =='POST':
        if request.user.is_authenticated:
            id=Roles.objects.get(role_name='Admin',deleted_status=False)
            check_admin=UserRole.objects.filter(user=request.user.id,role_id = id.pk,deleted_status=False).first()
            roles_data = json.loads(request.body)
            name=roles_data.get('name')
            if name is None or not name:
                return JsonResponse({'message':'Missing Required Filed or Key'},status=400)

            if check_admin: 
                role_exist , created= Roles.objects.get_or_create(
                    role_name = name,
                    added_by = check_admin.user,
                    deleted_status=False,
                    )
                if created:
                    
                    return JsonResponse({'message':f'{name} added successfully as role'})
                else:
                    return JsonResponse({'message':f'{name} already exist as Role'},status=409)
            else:
                return JsonResponse({'message':'user is not admin'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated '},status=401)
        
    elif request.method == "PUT":
        if request.user.is_authenticated:
            id=Roles.objects.get(role_name='Admin',deleted_status=False)
            check_admin=UserRole.objects.filter(user=request.user.id,role_id = id.pk,deleted_status=False).first()
            user_exist = User.objects.get(pk = request.user.id)

            load = json.loads(request.body)
            new_name=load.get('new_name')
            role_id=load.get('role_id')
            if new_name is None or role_id is None or not new_name or not role_id:
                return JsonResponse({'message':'Missing Required Filed or Key'},status=400)
            if check_admin:
                role_check=Roles.objects.filter(pk=role_id).first()
                if role_check:
                    Roles.objects.filter(pk=role_id).update(role_name=new_name)
                    return JsonResponse({'message':f'{role_check.role_name} updates with {new_name}'})
                else:
                    return JsonResponse({'message':'data not found '},status=204)
            else:
                return JsonResponse({'message':'user is not admin'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated '},status=401)

    elif request.method=='DELETE':
        if request.user.is_authenticated:
            id=Roles.objects.get(role_name='Admin',deleted_status=False)
            check_admin=UserRole.objects.filter(user=request.user.id,role_id = id.pk,deleted_status=False).first()
            if check_admin:
                id=request.GET.get('id')
                deleted=Roles.objects.filter(pk=id).first()
                if deleted:
                    Roles.objects.filter(pk=id).update(deleted_status=True,deleted_time=datetime.today())
                    return JsonResponse({'message':f'{deleted.role_name} deleted Successfully'})
                else:
                    return JsonResponse({'message':'Any role for this id cannot present'},status=204)
            else:
                return JsonResponse({'message':'You Are Not Admin'},status=403)
        else:
            return JsonResponse({'message':'You Are Not Authenticated'},status=401)
    else:
        return JsonResponse({'message':'invalid request method'},status=405)



def child(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            id=Roles.objects.get(role_name='Admin',deleted_status=False)
            check_admin=UserRole.objects.filter(user=request.user.id,role_id = id.pk,deleted_status=False).first()
            if check_admin:   
                load = json.loads(request.body)
                id = load.get('id')
                name = load.get('name')
                parent=Dropdown.objects.filter(id = id, child__gt=0).first()
                if parent is not None:
                    dropdown, created=Dropdown.objects.get_or_create(
                        name= name,
                        added_by=check_admin.user,
                        relation_id = parent.pk,
                        child = int(parent.child) -1,
                        deleted_status=False
                    )
                    if created:
                        return JsonResponse({'message':f'{name} successfully added for {parent.name}'})
                    else:
                        return JsonResponse({'message':f'{name} already exist for this {parent.name}'},status=409)
                else:
                    return JsonResponse({'message':f'Child cannot be added for this parent'},status=409)
            else:
                return JsonResponse({'message':'user is not admin'})
        else:
            return JsonResponse({'message':'user is not authenticated'})
    
    elif request.method=='PUT':
        if request.user.is_authenticated:
            id=Roles.objects.get(role_name='Admin',deleted_status=False)
            check_admin=UserRole.objects.filter(role_id = id.pk,deleted_status=False).first()
            if check_admin:
                load=json.loads(request.body)
                id = load.get('id')
                new_name = load.get('new_name')
                parent=Dropdown.objects.filter(id = id).first()
                if parent:
                    Dropdown.objects.filter(pk=id).update(name=new_name)
                    return JsonResponse({'message':f'{parent.name} updates with {new_name}'},status=201)
                else:
                    return JsonResponse({'message':'data not found'},status=409)
            else:
                return JsonResponse({'message':'user is not admin'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
        
    elif request.method=='DELETE':
        if request.user.is_authenticated:
            id=Roles.objects.get(role_name='Admin',deleted_status=False)
            check_admin=UserRole.objects.filter(role_id = id.pk,deleted_status=False).first()
            if check_admin:
                id=request.GET.get('id')
                deleted=Dropdown.objects.filter(pk=id).first()
                if deleted:
                    Dropdown.objects.filter(pk=id).update(deleted_status=True,deleted_time=datetime.now())
                    return JsonResponse({'message':f'{deleted.name} deleted Successfully'})
                else:
                    return JsonResponse({'message':'No child Found'},status=204)
            else:
                return JsonResponse({'message':'You Are Not Admin'},status=403)
        else:
            return JsonResponse({'message':'You Are Not Logged In'},status=401)

    else:
        return JsonResponse({'message':'Invalid Reqest Method'},status=405)            

def left_panel(request):
    if request.user.is_authenticated:
        id=Roles.objects.get(role_name='Admin',deleted_status=False)
        check_admin=UserRole.objects.filter(user=request.user.id,role_id = id.pk,deleted_status=False).first()
        if check_admin:
            if request.method == 'POST':
                load=json.loads(request.body)
                name=load.get('name')
                state=load.get('state')
                icon=load.get('icon')
                type=load.get('type')
                role=load.get('role')
                panel,created=Dropdown.objects.get_or_create(name=name,                   
                state=state,                              
                icon=icon,                               
                type=type,                               
                role=role,                               
                pannel=1,
                defaults={ "added_by":check_admin.user}
               
                )
                if created:
                    return JsonResponse({'message':f'{name} successfully added for SideBar'},status=201)
                else:
                    return JsonResponse({'message':f'Already Exist {name}'},status=409)
            
            elif request.method == 'PUT':
                load=json.loads(request.body)
                id=load.get('id')
                name=load.get('name')
                state=load.get('state')
                icon=load.get('icon')
                type=load.get('type')
                role=load.get('role')
    
                
                update_panel=Dropdown.objects.filter(pk=id,deleted_status=False).update(name=name,                   
                state=state,                              
                icon=icon,                               
                type=type,                               
                role=role,                               
                )
                if update_panel:
                    return JsonResponse({'message':'Updated successfully'},status=200)
                else:
                    return JsonResponse({'message':'Panel not found'},status=400)
    
            else:
                return JsonResponse({'message':'Invalid Request Method'},status=405)
        else:
                return JsonResponse({'message':'You are not autherised'},status=403)
    else:
        return JsonResponse({'message':'You are not logged in'},status=401)
    
    

    





        





