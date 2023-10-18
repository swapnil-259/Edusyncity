from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import json
import re
from .models import User,Roles, UserRole, Faculty,Dropdown,Mapping, Student,Subjects
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from datetime import datetime,date


def register_faculty(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if UserRole.objects.filter(user=request.user.id,role_id = '1').first():
                load= json.loads(request.body)
                first_name = load.get('firstname')
                last_name = load.get('lastname')
                user_name =  load.get('username')
                email =  load.get('email')
                gender =  load.get('gender')
                contact =  load.get('contact')
                age =  load.get('age')
                address =  load.get('address')
                department =  load.get('department')
                qualification = load.get('qualification')
                title = load.get('title')
                subject =  load.get('subject')
                course = load.get('course')
                religion = load.get('religion')
                if not user_name or not first_name or not last_name or not email or not gender or not contact or not age or not address or not department or not qualification or not title or not subject or not course or not religion:
                      return JsonResponse({'message':'Missing Required Field'}, status = 400)
                if user_name is None or email is None or first_name is None or last_name is None or  age is None or gender is None or contact is None or address is None or qualification is None or title is None or subject is None or course is None or religion is None:
                    return JsonResponse({'messge':'Missing any key'},status=400) 
                
                if not re.match(r'^[6-9]\d{9}$',contact):
                    return JsonResponse({'message':'Your Contact Can have only 10 digits and in indian Format'},status=400)
                if not re.match(r'^[a-zA-Z0-9_@-]{8,15}$',user_name):
                    return JsonResponse({'message':'Match Your Username Requirements'},status=400)
                if not re.match(r'^[A-Za-z\s]+$', first_name):
                    return JsonResponse({'message':'Invalid first_name format'},status=400)
                if not re.match(r'^[A-Za-z\s]+$', last_name):
                    return JsonResponse({'message':'Invalid last_name format'},status=400)
                if not re.match(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b',email):
                    return JsonResponse({'message':'Match Your email Requirements'},status=400)
                if int(age) < 0:
                    return JsonResponse({'message':'Age Can Not Be Negative '},status=400)
                
                gender_exist = Dropdown.objects.filter(id = gender ).first()
                if gender_exist is None:
                    return JsonResponse({'message':'Gender Not an instance'},status=400)
                department_exist = Mapping.objects.filter(id = department).first()
                if department_exist is None:
                    return JsonResponse({'message':'Department Not an Instance'},status=400)
                title_exist = Dropdown.objects.filter(id = title).first()
                if title_exist is None:
                    return JsonResponse({'message':'Title Not an Instance'},status=400)
                subject_exist = Subjects.objects.filter(id = subject).first()
                if subject_exist is None:
                    return JsonResponse({'message':'Subject Not an Instance'},status=400)
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
                
                user=  User.objects.create_user(
                username = user_name,
                password = "Kiet@123",
                first_name=first_name,
                last_name=last_name,
                email=email
                ) 
                Faculty.objects.create(
                user_id = user.id,
                department = department_exist,
                subject = subject_exist,
                qualification = qualification,
                address = address,
                title = title_exist,
                course = course_exist,
                religion = religion_exist
                )
                roles, created = Roles.objects.get_or_create(role_name= 'Faculty')
                if not created:
                    return JsonResponse({'message':'You Already Have This Role'},status=409)
                else:
                    UserRole.objects.create(
                    user_id = user.id,
                    role_id = roles.id,
                    )
                    return JsonResponse({'message':'Registration Succesfull'},status=201)
            else:
                return JsonResponse({'message':'You are not Admin'},status=403)
        else:
            return JsonResponse({'message':'You are not Authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)
def register_student(request):
    if request.method == 'POST':
        load=json.loads(request.body)
        first_name = load.get('first_name')
        last_name = load.get('last_name')
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
        if not user_name or not first_name or not last_name or not email or not gender or not contact or not age or not address or not department or not father_name or not mother_name or not year or not course or not religion:
                      return JsonResponse({'message':'Missing Required Field'}, status = 400)
        if user_name is None or email is None or first_name is None or last_name is None or  age is None or gender is None or contact is None or address is None or father_name is None or mother_name is None or year is None or course is None or religion is None:
                    return JsonResponse({'messge':'Missing any key'},status=400) 
                
        if not re.match(r'^[6-9]\d{9}$',contact):
            return JsonResponse({'message':'Your Contact Can have only 10 digits and in indian Format'},status=400)
        if not re.match(r'^[a-zA-Z0-9_@-]{8,15}$',user_name):
            return JsonResponse({'message':'Match Your Username Requirements'},status=400)
        if not re.match(r'^[A-Za-z\s]+$', first_name):
            return JsonResponse({'message':'Invalid first_name format'},status=400)
        if not re.match(r'^[A-Za-z\s]+$', father_name):
            return JsonResponse({'message':'Invalid first_name format'},status=400)
        if not re.match(r'^[A-Za-z\s]+$', mother_name):
            return JsonResponse({'message':'Invalid first_name format'},status=400)
        if not re.match(r'^[A-Za-z\s]+$', last_name):
            return JsonResponse({'message':'Invalid last_name format'},status=400)
        if not re.match(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b',email):
            return JsonResponse({'message':'Match Your email Requirements'},status=400)
        if int(age) < 0:
            return JsonResponse({'message':'Age Can Not Be Negative '},status=400)
        
        gender_exist = Dropdown.objects.filter(id = gender ).first()
        if gender_exist is None:
            return JsonResponse({'message':'Gender Not an instance'},status=400)
        department_exist = Mapping.objects.filter(id = department).first()
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
            first_name= first_name,
            last_name=last_name,
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
            contact= contact,
            course = course_exist,
            father_name = father_name,
            mother_name= mother_name,
            religion = religion_exist
        )
        roles, created = Roles.objects.get_or_create(role_name= 'Student')

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
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$",new_password):
            return JsonResponse({'message':'Match Your Password Requirements'},status=400)
        
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
            if check_admin: 
                role_exist , created= Roles.objects.get_or_create(
                    role_name = name,
                    added_by = user_exist,
                    deleted_status=False,
                    )
                if created:
                    
                    return JsonResponse({'message':'role successfully added'},status=201)
                else:
                    return JsonResponse({'message':'role already exist'},status=409)
            else:
                return JsonResponse({'message':'user is not admin'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated '},status=401)
        
    elif request.method == "PUT":
        load = json.loads(request.body)
        new_name=load.get('new_name')
        role_id=load.get('role_id')
        if new_name is None or role_id is None or not new_name or not role_id:
            return JsonResponse({'message':'Missing Required Filed or Key'},status=400)
        if request.user.is_authenticated:
            check_admin = UserRole.objects.filter(role_id = '1').first()
            user_exist = User.objects.get(pk = request.user.id)
    
            if check_admin:
                Roles.objects.filter(pk=role_id).update(role_name=new_name)
                return JsonResponse({'message':'Role Updated Successfully'},status=200)
            else:
                return JsonResponse({'message':'user is not admin'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated '},status=401)

    elif request.method=='DELETE':
        if request.user.is_authenticated:
            if UserRole.objects.filter(role_id = '1').exists():
                id=request.GET.get('id')
                deleted=Roles.objects.filter(pk=id).update(deleted_status=True,deleted_time=datetime.today())
                if deleted:
                    return JsonResponse({'message':'Role Deleted Successfully'},status=200)
                else:
                    return JsonResponse({'message':'No Role Found'},status=204)
            else:
                return JsonResponse({'message':'You Are Not Admin'},status=403)
        else:
            return JsonResponse({'message':'You Are Not Logged In'},status=401)
    else:
        return JsonResponse({'message':'invalid request method'},status=405)


def add_course(request):
    
    if request.method == 'POST':
        course_data = json.loads(request.body)
        course_name = course_data.get('course_name')
        child_count = course_data.get('child_count')
        state = course_data.get('state')
        type = course_data.get('type')
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
                    can_update = True,
                    state = state,
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
    


def dropdown(request):
    if request.method == 'POST':
        load = json.loads(request.body)
        if request.user.is_authenticated:
            check_admin = UserRole.objects.filter(role_id = '1', user_id = request.user.id).first()
            if check_admin:
                id = load.get('id')
                name = load.get('name')
                parent=Dropdown.objects.filter(id = id, child__gte=0).first()
                if parent is not None:
                    dropdown, created=Dropdown.objects.get_or_create(
                        name= name,
                        added_by=check_admin.user,
                        relation_id = parent.pk,
                        child = int(parent.child) -1,
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
        
    elif request.method=='PUT':
        if request.user.is_authenticated:
            check_admin = UserRole.objects.filter(role_id = '1', user_id = request.user.id).first()
            if check_admin:
                load=json.loads(request.body)
                id = load.get('id')
                new_name = load.get('new_name')
                parent=Dropdown.objects.filter(id = id).exists()
                if parent is not None:
                    updated=Dropdown.objects.filter(pk=id).update(name=new_name)
                    
                    if updated:
                        return JsonResponse({'message':'dropdown updated successfully'},status=201)
                    else:
                        return JsonResponse({'message':'dropdown does not exists'},status=204)
                else:
                    return JsonResponse({'message':'You can not add child for this Parent'},status=409)
                
            else:
                return JsonResponse({'message':'user is not admin'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
        
    elif request.method=='DELETE':
        if request.user.is_authenticated:
            if UserRole.objects.filter(role_id = '1').exists():
                id=request.GET.get('id')
                deleted=Dropdown.objects.filter(pk=id).update(deleted_status=True,deleted_time=datetime.now())
                if deleted:
                    return JsonResponse({'message':'Role Deleted Successfully'},status=200)
                else:
                    return JsonResponse({'message':'No Role Found'},status=204)
            else:
                return JsonResponse({'message':'You Are Not Admin'},status=403)
        else:
            return JsonResponse({'message':'You Are Not Logged In'},status=401)

    else:
        return JsonResponse({'message':'Invalid Reqest Method'},status=405)
    

                
                
                        
            
            

        
        





