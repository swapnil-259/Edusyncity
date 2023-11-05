from django.shortcuts import render
from django.http import JsonResponse
import json
import re
from .models import User,Roles, UserRole, Faculty,Dropdown,Mapping, Student
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from datetime import datetime,date
from EduCore.views import check_user
from django.db.models import Q

def validation(email = None,firstname = None,lastname = None,fathername = None, mothername = None):
    
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
    

def faculty_validation(load):
    
    keys_to_check = ['firstname', 'lastname', 'username', 'email', 'gender','contact','age','qualification','title','address']
    
    for key in keys_to_check:
        if key not in load:
            return JsonResponse({'message': f'{key} is missing'}, status=400)  
        
        value=str(load[key]).strip()
        if value == '':
            return JsonResponse({'message': f'{key} can not be space or none'}, status=400)
        
        elif key == 'age':
            if not value.isdigit():
                return JsonResponse({'message':f'{key} accept only integer'},status=400)
            
        elif key == 'title':
            if not value.isdigit():
                return JsonResponse({'message':f'{key} accept only integer'},status=400)
            
        elif key == 'contact':
            if not value.isdigit():
                return JsonResponse({'message':f'{key} accept only integer'},status=400)

def register_faculty(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            admin = check_user(request.user.id, 'Admin')

            if admin:
                load= json.loads(request.body)
                firstname = load.get('firstname')
                lastname = load.get('lastname')
                username =  load.get('username')
                email =  load.get('email')
                gender =  load.get('gender')
                contact =  load.get('contact')
                age =  load.get('age')
                address =  load.get('address')
                qualification = load.get('qualification')
                title = load.get('title')
                
                if age is ' ' or int(age) <= 25:
                    return JsonResponse({'message':'Age Can Not Be Negative or blank space'},status=400)
                
                if not username or not firstname or not lastname or not email or not gender or not contact or not age or not address  or not qualification or not title :
                      return JsonResponse({'message':'Missing Required Field'}, status = 400)
                  
                if username is None or email is None or firstname is None or lastname is None or  age is None or gender is None or contact is None or address is None or qualification is None or title is None :
                    return JsonResponse({'messge':'Missing any key'},status=400) 
                
                if username is ' ' or email is ' ' or firstname is ' ' or lastname is ' ' or age is ' ' or gender is ' ' or contact is ' ' or address is ' ':
                    return JsonResponse({'messsage':'You Are Passing Space to the Field'},status=400)
                
                validation_data =   validation(firstname=firstname, lastname=lastname, email=email, age=age)
                if validation_data:
                  return validation_data
              
                check=faculty_validation(load)
                if check:
                    return check

                gender_exist = Dropdown.objects.filter(id = gender ).first()
                if gender_exist is None:
                    return JsonResponse({'message':'Gender Not an instance'},status=400)
                
                title_exist = Dropdown.objects.filter(id = title).first()
                if title_exist is None:
                    return JsonResponse({'message':'Title Not an Instance'},status=400)
                
                if User.objects.filter(username=username).first():
                    return JsonResponse({'message':'Username Already exists'},status=409)
                
                elif User.objects.filter(email=email).first():
                    return JsonResponse({'message':'Email Already exists'},status=409)
                
                user=  User.objects.create_user(
                username = username,
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
                added_by = admin,
                age = age,
                gender = gender_exist
                )
                
                roles, created = Roles.objects.get_or_create(role_name= 'Teacher')
                UserRole.objects.create(
                    user_id = user.id,
                    role_id = roles.id,
                    added_by = admin
                    )
                return JsonResponse({'message':'registration Successful'},status=201)

            else:
                return JsonResponse({'message':'You are not Admin'},status=403)
        else:
            return JsonResponse({'message':'You are not Authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)

def get_personal_info(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            faculty=check_user(request.user.id,'Teacher')
            student=check_user(request.user.id,'Student')
            admin=check_user(request.user.id,'Admin')
            if faculty:
                info=list(Faculty.objects.filter(deleted_status=False,user=request.user.id).values('title__name','user__first_name','user__last_name','age','gender__name','address','contact','qualification'))
                if info:
                    return JsonResponse({'t_detail':info})
                else:
                    return JsonResponse({'message':'no data found'},status=204)
            elif student:
                info=list(Student.objects.filter(deleted_status=False,user=request.user.id).values('user__first_name','user__last_name','age','gender__name','address','contact','father_name','mother_name','course__name','department__department__name','year','religion__name'))
                if info:
                    return JsonResponse({'s_detail':info})
                else:
                    return JsonResponse({'message':'no data found'},status=204)
            elif admin:
                relation=Dropdown.objects.filter(name='Courses').first()
                courses = Dropdown.objects.filter(relation_id=relation.pk).all()
                data = {
                    'course_name':[],
                    'department_count':[]
                }   

                for course_id in courses:
                    department_count = Mapping.objects.filter(course_id=course_id.id).count()
                    data['course_name'].append(course_id.name)
                    data['department_count'].append(department_count)
                return JsonResponse(data, safe=False)

            else:
                return JsonResponse({'message':'you are not autherised'},status=403)
        else:
            return JsonResponse({'message':'You are not logged in'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)


def register_student(request):
    
    if request.method == 'POST':
        
         if request.user.is_authenticated:
            admin = check_user(request.user.id, 'Admin')

            if admin:
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
                print(admin)
                # try:
                #     firstname = load['first_name'] 
                # except:
                #     return JsonResponse({'message':'firstname is missing'},status=400) 

                # for key in load:
                #     if key not in load:
                #         return JsonResponse({'message':'firstname is missing'},status=400) 
                # value=load.keys()
                # if 'first_name' not in value:
                #     return JsonResponse({'message':'firstname is missing'},status=400) 
                 
                
                if age is ' ' or int(age) < 16:
                    return JsonResponse({'message':'Age Can Not Be Negative or blank space'},status=400)

                if not user_name or not firstname or not lastname or not email or not gender or not contact or not age or not address or not department or not father_name or not mother_name or not year or not course or not religion:
                              return JsonResponse({'message':'Missing Required Field'}, status = 400)
                          
                if user_name is None or email is None or firstname is None or lastname is None or  age is None or gender is None or contact is None or address is None or father_name is None or mother_name is None or year is None or course is None or religion is None:
                            return JsonResponse({'messge':'Missing any key'},status=400) 
                        
                if user_name is ' ' or email is ' ' or firstname is ' ' or lastname is ' ' or age is ' ' or gender is ' ' or contact is ' ' or address is ' ':
                    return JsonResponse({'messsage':'You Are Passing Space to the Field'},status=400)
                
                validation_data = validation(firstname=firstname, lastname=lastname, email=email, fathername=father_name, mothername=mother_name)
                if validation_data:
                    return validation_data
                
                gender_exist = Dropdown.objects.filter(id = gender ).first()
                if gender_exist is None:
                    return JsonResponse({'message':'Gender Not  found'},status=400)
                
                department_exist = Mapping.objects.filter(id = department).first()
                if department_exist is None:
                    return JsonResponse({'message':'Department Not found'},status=400)
                
                course_exist = Dropdown.objects.filter(id = course).first()
                if course_exist is None:
                    return JsonResponse({'message':'Course Not found'},status=400)
                
                religion_exist = Dropdown.objects.filter(id = religion).first()
                if religion_exist is None:
                    return JsonResponse({'message':'Religion Not found'},status=400)
                
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
                    added_by = admin
                )
                
                roles, created = Roles.objects.get_or_create(role_name= 'Student')
                UserRole.objects.create(
                    user_id = user.id,
                    role_id = roles.id,
                    added_by = admin                    )
                return JsonResponse({'message':'registration Successful'},status=201)
            else:   
                return JsonResponse({'message':'user is not admin'},status=403)
         else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)



def login_user(request):
    if request.method == 'POST':
        #  m = User.objects.get(username=request.POST["username"])
        #  if m.check_password(request.POST["password"]):
        #       login(request,m)
        #     #   request.session=m.id
        #       return JsonResponse({"message":"user logged in"})
        #  else:
        #       return JsonResponse({"message":"user  not logged in"})
             

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
            return JsonResponse({'message':'Incorrect username or password'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)

def change_password(request):
    
    if request.method == 'POST':
        
        load_data=json.loads(request.body)
        username = load_data.get('username')
        old_password = load_data.get('old_password')
        new_password = load_data.get('new_password')
        
        if username is None or old_password is None or new_password is None:
            return JsonResponse({'message':'Missing any Key.'})
        
        if not new_password or not old_password or not username:
              return JsonResponse({'message': 'Missing Required field.'}, status=400)
    
        if not re.match(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-_]).{8,}$",new_password):
            return JsonResponse({'message':'Password Requirements min length 8, atleast 1 upercase and lowercase and numeric, allowed special characters #?!@$%^&*-_'},status=400)

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
           
            admin = check_user(request.user.id, 'Admin')
            roles_data = json.loads(request.body)
            name=roles_data.get('name')
            
            if name is None or not name:
                return JsonResponse({'message':'Missing Required Filed or Key'},status=400)

            if admin: 
                role_exist , created= Roles.objects.get_or_create(
                    role_name = name,
                    added_by = admin,
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
           
            admin = check_user(request.user.id, 'Admin')

            load = json.loads(request.body)
            new_name=load.get('new_name')
            role_id=load.get('role_id')
            
            if new_name is None or role_id is None or not new_name or not role_id:
                return JsonResponse({'message':'Missing Required Filed/Key'},status=400)
            
            if admin:
                role_check=Roles.objects.filter(pk=role_id,deleted_status=False).first()
                if role_check:
                    
                    Roles.objects.filter(pk=role_id,deleted_status=False).update(role_name=new_name)
                    return JsonResponse({'message':f'{role_check.role_name} updates with {new_name}'})
                
                else:
                    return JsonResponse({'message':'data not found '},status=204)
            else:
                return JsonResponse({'message':'user is not admin'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated '},status=401)

    elif request.method=='DELETE':
        
        if request.user.is_authenticated:
           
            admin = check_user(request.user.id, 'Admin')
            
            if admin:
                
                id=request.GET.get('id')
                deleted=Roles.objects.filter(pk=id,deleted_status=False).first()
                
                if deleted:
                    Roles.objects.filter(pk=id,deleted_status=False).update(deleted_status=True,deleted_time=datetime.today())
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
    if request.user.is_authenticated:
       
        admin = check_user(request.user.id, 'Admin')
        if admin:   
            
            if request.method == 'POST':
                
                load = json.loads(request.body)
                id = load.get('id')
                name = load.get('name')
                
                if id is None or name is None or not id or not name:
                    return JsonResponse({'message':'Missing required field or key'},status=400)
                
                parent=Dropdown.objects.filter(id = id, child__gt=0,deleted_status=False).first()
                if parent is not None:
                    
                    dropdown, created=Dropdown.objects.get_or_create(
                        name= name,
                        relation_id = parent.pk,
                        child = int(parent.child) -1,
                        deleted_status=False,
                        can_delete=parent.can_delete,
                        can_update=parent.can_update,
                        defaults={"added_by":admin}
                    )
                    
                    if created:
                        return JsonResponse({'message':f'{name} successfully added for {parent.name}'})
                    else:
                        return JsonResponse({'message':f'{name} already exist for this {parent.name}'},status=409)
                else:
                    return JsonResponse({'message':f'Child cannot be added for this parent'},status=409)
            
            elif request.method == 'PUT':
                
                load=json.loads(request.body)
                id = load.get('id')
                new_name = load.get('new_name')
                
                if id is None or new_name is None or not id or not new_name:
                    return JsonResponse({'message':'Missing any key or field'},status=400)
                
                parent=Dropdown.objects.filter(id = id,deleted_status=False).first()
                if parent:
                    Dropdown.objects.filter(pk=id,deleted_status=False).update(name=new_name)
                    return JsonResponse({'message':f'{parent.name} updates with {new_name}'},status=201)
                
                else:
                    return JsonResponse({'message':'Parent not match'},status=400)
            
            elif request.method == 'DELETE':
                
                id=request.GET.get('id')
                if id is None or not id:
                    return JsonResponse({'message':'Expecting an id'},status=400)
                
                deleted=Dropdown.objects.filter(pk=id,deleted_status=False).first()
                if deleted:
                    Dropdown.objects.filter(pk=id,deleted_status=False).update(deleted_status=True,deleted_time=datetime.now())
                    return JsonResponse({'message':f'{deleted.name} deleted Successfully'})
                
                else:
                    return JsonResponse({'message':'No child Found'},status=204)
            else:
                return JsonResponse({'message':'Invalid Reqest Method'},status=405)
        else:
            return JsonResponse({'message':'You are not autherised'},status=403)
    else:
        return JsonResponse({'message':'You are not authenticated'},status=401)

   

def left_panel(request):
    if request.user.is_authenticated:
      
        admin = check_user(request.user.id, 'Admin')
        if admin:
            
            if request.method == 'POST':
                load=json.loads(request.body)
                name=load.get('name')
                state=load.get('state')
                icon=load.get('icon')
                type=load.get('type')
                role=load.get('role')

                if name is None or state is None or icon is None or type is None or role is None:
                    return JsonResponse({'return':'Missing any key'},status=400)
                if not name or not state or not icon or not type or not role:
                    return JsonResponse({'message':'Missing required field'},status=400)

                panel,created=Dropdown.objects.get_or_create(
                name=name,                   
                state=state,                                                             
                type=type,                               
                role=role,                               
                pannel=1,
                deleted_status=False,
                defaults={ "added_by":admin,"role":role}
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
                
                if name is None or state is None or icon is None or type is None or role is None:
                    return JsonResponse({'return':'Missing any key'},status=400)
                if not name or not state or not icon or not type or not role:
                    return JsonResponse({'message':'Missing required field'},status=400)
                
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

# def s

    

    





        





