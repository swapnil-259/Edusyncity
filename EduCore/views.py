from django.shortcuts import render

import json
from django.http import JsonResponse,HttpResponse
from EduAdmin.models import UserRole,Dropdown,Mapping,User,Roles,Faculty
from datetime import datetime,date
from .models import Subject
from EduCore.models import Subject,SubjectMapping,SubjectTeacherMapping
import re

def logged_in(request):
    
    if request.method == 'GET':
        
        if request.user.is_authenticated:
            user_data=UserRole.objects.filter(user=request.user.id,deleted_status=False).first()
            username=User.objects.filter(pk=user_data.user_id).first()
            
            if user_data and username:
                return JsonResponse({'role_id':user_data.role_id,'username':username.username,'first_name':username.first_name,'last_name':username.last_name})
            
            else:
                return JsonResponse({'message':'User not found'},status=401)
        else:
            return JsonResponse({'message':'You are not Authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)
    


def get_parents(request):
    
    if request.method == 'GET':
        
        if request.user.is_authenticated:
            
            data=Dropdown.objects.filter(deleted_status=False,child__gt=0,pannel=0).values('id','name','child','can_delete','can_update')
            if data is None:
                return JsonResponse({'message':'Courses Not Found'},status=204)
            
            else:
                return JsonResponse(list(data),safe=False)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)
    

def parents(request):
    
    if request.user.is_authenticated:
        
         check_Admin=check_user(request.user.id, 'Admin')
         if check_Admin:
             
          if request.method=='POST':
                load = json.loads(request.body)
                name = load.get('name')
                depth = load.get('depth')
                can_edit = load.get('editable')
                can_delete=load.get('deletable')
                
                if name is None or depth is None:
                    return JsonResponse({'message':'missing field'},status=400)
                if not name or not depth:
                    return JsonResponse({'message':'required Field'},status=400)
                if not re.match(r'^[A-Za-z\s]+$',name):
                    return JsonResponse({'message':'Invalid name format'},status=400)
                
                parent, created = Dropdown.objects.get_or_create(
                    name=name,
                    defaults={"added_by":check_Admin,
                    "can_delete":can_delete,
                     "child":depth ,
                    "can_update":can_edit}
                    )
                
                if created:
                    return JsonResponse({'message':f'{name} created successfully as Parent'},status=201)
                else:
                    
                    if parent.deleted_status=='0':
                        Dropdown.objects.create(
                        name=name,
                        added_by=check_Admin,
                        can_delete=can_delete,
                        child=depth ,
                        can_update=can_edit)
                        return JsonResponse({'message':'created Successfully'},status=201)
                    
                    else: 
                        return JsonResponse({'message':f'This {name} already exist as Parent'},status=409)
                    
          elif request.method =='DELETE':
                      id = request.GET.get('id')
                      Dropdown.objects.filter(id =id).update(deleted_status=True, deleted_time=datetime.now())
                      return JsonResponse({'message':'deleted successfully'})
                  
          elif request.method=='PUT':
              
              load = json.loads(request.body)
              id = load.get('id')
              name = load.get('name')
              Dropdown.objects.filter(id=id).update(name = name)
              return JsonResponse({"message":'Parent updated successfully'})
          
          else:
                return JsonResponse({'message':'invalid request method'},status=405)
         else:
            return JsonResponse({'message':'You are not Admin'},status=403)
    else:
        return JsonResponse({'message':'You not not Authenticated'},status=401)
    
def check_user(user, user_role):
    
        role=Roles.objects.filter(role_name=user_role,deleted_status=False).first()
        if role:
            
          user_with_role=UserRole.objects.filter(user=user,role_id = role.id,deleted_status=False).first()
          if user_with_role:
              return user_with_role.user
          
          else:
              return None
        else:
            return None

            
            
def get_childs(request):
    
    if request.method == 'GET':
        
        if request.user.is_authenticated:
            
            parent_id=request.GET.get('parent_id')
            data=Dropdown.objects.filter(relation=parent_id,deleted_status=False).values('id','name')
            if data is None:
                return JsonResponse({'message':'Childs Not Found'},status=204)
            
            else:
                return JsonResponse(list(data),safe=False)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)
    
    
def departments(request):
    
    if request.method == 'GET':
        
        if request.user.is_authenticated:
            
            id = request.GET.get('course_id')
            data=Mapping.objects.filter(deleted_status=False, course=id).values('department__name','id')
            if data is None:
                return JsonResponse({'message':'Courses Not Found'},status=204)
            
            else:
                return JsonResponse(list(data),safe=False)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)



def years(request):
    
    if request.method == 'GET':
        
        if request.user.is_authenticated:
            
            course_id=request.GET.get('course_id')
            data=Dropdown.objects.filter(pk=course_id,deleted_status=False).first()
            year_data = data.year
            years=[]
            
            for i in range(1,int(year_data)+1):
                years.append(i)
            return JsonResponse(years,safe=False)
        
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)


def subjects(request):
    
    if request.method == 'GET':
        
        if request.user.is_authenticated:
            
            subjects=Subject.objects.filter(deleted_status=False).values('id','subject_name','subject_code')
            if subjects:
                return JsonResponse(list(subjects),safe=False)
            
            else:
                return JsonResponse({'message':'Subject Not Found'},status=204)
        else:
            return JsonResponse({'message':'user is not authenticated'}, status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)

     
def sidebar(request):
    
    if request.method == 'GET':
        
        if request.user.is_authenticated:
            
             check_user = UserRole.objects.filter(user =request.user.id).first()
             leftpanel = []
             child=[]
             
             if check_user:
                pannels = Dropdown.objects.filter(pannel=1,deleted_status=False, role = check_user.role.id).values('id')
                
                if not pannels or pannels is None:
                    return JsonResponse({'message':'Missing Required Field or Key'},status=400)
                
                for i in pannels:
                    child_data = list(Dropdown.objects.filter(relation_id = i.get('id'),deleted_status=False,role = check_user.role.id).values('name','state','icon'))
                    child.append(child_data)
                master_configuration = Dropdown.objects.filter(pannel=1,deleted_status=False,role=check_user.role.id).values('pk','name','icon','type','state')
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
            admin = check_user(request.user.id, 'Admin')

            if admin:
                subject_name = data.get('subject_name')
                subject_code = data.get('subject_code')   
                
                if not subject_name or not subject_code:
                    return JsonResponse({'message':'missing required field'},status=400)  
                 
                if subject_code is None or subject_name is None :
                    return JsonResponse({'message':'missing any key'},status=400)
                
                subjects , created = Subject.objects.get_or_create(
                subject_name= subject_name,
                subject_code=subject_code,
                added_by=admin
                
                ) 
                
                if created:
                   return JsonResponse({'message':f'{subject_name} added successfully'},status=201)
                else:
                   return JsonResponse({'message':f'{subject_name} already exist'}, status = 409)
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
            admin = check_user(request.user.id, 'Admin')

            if admin:
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
                
                department_exist = Mapping.objects.filter(id = department).first()
                if department_exist is None:
                    return JsonResponse({'message':'department not found'},status=204)
                
                subject_mapping, created=SubjectMapping.objects.get_or_create(
                    subject=subject_exist,
                    department=department_exist,
                    year=year,
                    added_by=admin
                )
                
                if created:
                    return JsonResponse({'message':f'{subject_exist.subject_name} mapped successfully with {department_exist.department.name} department for this {year}rd year'})
                else:
                    return JsonResponse({'message':f'{subject_exist.subject_name} is already mapped with this {department_exist.department.name} for {year}rd yaer'},status=409)
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
            
            admin = check_user(request.user.id, 'Admin')

            if admin:
                sub_mapping = data.get('sub_mapping_id')
                faculty = data.get('faculty_id')
                
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
                defaults={"added_by" : admin}
                )
                
                if created:
                    return JsonResponse({'message':f'{sub_mapping_exist.subject.subject_name} mapped successfully with {faculty_exist.title.name} {faculty_exist.user.first_name} {faculty_exist.user.last_name}'})
                else:
                    return JsonResponse({'message':f'{sub_mapping_exist.subject.subject_name} already mapped for {faculty_exist.title.name} {faculty_exist.user.first_name} {faculty_exist.user.last_name}'},status=409)
            else:
                return JsonResponse({'message':'user is not admin'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'invalid request method'},status=405)
    
    
def dropdown_option(request,dropdown):
    
    if request.method =='GET':
        
        if request.user.is_authenticated:
            
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
            elif dropdown=='shift':
                name = 'Shift'
                return dropdown_value(name)
            elif dropdown=='examtype':
                name = 'Exam Type'
                return dropdown_value(name)
            elif dropdown =='duration':
                name = 'Duration'
                return dropdown_value(name)
            elif dropdown =='marks':
                name='Marks'
                return dropdown_value(name)
            elif dropdown=='Set':
                return dropdown_value(dropdown)
            else:
                return JsonResponse({'message':"no url found"})
        
        else:
            return JsonResponse({"message":"User is not Authenticated"},status=404)
    else:
        return JsonResponse({'message':'Invalid request method'}, status=40)
    
    
def dropdown_value(name):
    
    id=Dropdown.objects.filter(deleted_status=False,name=name,pannel=0).first() 
    mapping = Dropdown.objects.filter(relation_id = id.pk,deleted_status=False).values('id','name')
    
    if mapping:
            mapping_data = list(mapping)
            return JsonResponse(mapping_data, safe=False)
    else:
        return JsonResponse({'message':'data is not found'},status=204)
             
             
def assign_department_to_course(request):
    
    if request.method == 'POST':
        
        if request.user.is_authenticated:
            admin = check_user(request.user.id, 'Admin')

            if admin:
                    load=json.loads(request.body)
                    course_id = load.get('course_id')
                    department_id = load.get('department_id')
                    course_exist= Dropdown.objects.filter(pk = course_id).first()
                    department_exist = Dropdown.objects.filter(pk = department_id).first()
                    
                    if course_exist is not None and department_exist is not None:
                        mapping, created = Mapping.objects.get_or_create(course= course_exist, department = department_exist, defaults={"added_by" : admin} )
                        
                        if created:
                            return JsonResponse({'message':f'{department_exist.name} successfully mapped with {course_exist.name}'},status=201)
                        else:
                            return JsonResponse({'message':f'{department_exist.name} already mapped for this {course_exist.name}'},status=409)
                    else:
                        return JsonResponse({'message':'course/departemnt not exist'},status=204)
            else:
                return JsonResponse({'message':'user is not Admin'},status=403)
        else: 
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'invalid request method'},status=405)   
    
    
def get_departments(request):
    
    if request.method=='GET':
        
        if request.user.is_authenticated:
            
            dept_id = Dropdown.objects.filter(name='Departments',deleted_status=False).first()
            dept_data = Dropdown.objects.filter(relation=dept_id.id,deleted_status=False).values('name','id')
            if dept_data:
                return JsonResponse(list(dept_data),safe=False)
            
            else:
                return JsonResponse({'message':'data not found'},status=204)
        else:
            return JsonResponse({'message':'user is not authenticated'})
    else:
        return JsonResponse({'message':'invalid request method'},status=405)
    
    
def get_years(request):
    print(request)
    
    if request.method =='GET':
        
        if request.user.is_authenticated:
            
            id = request.GET.get('dept_mapped_id')
            mapping_exist = Mapping.objects.filter(id = id,deleted_status=False).first()
            
            if mapping_exist:
                year = mapping_exist.course.year
                years=[]
                for i in range(1,int(year)+1):
                    years.append(i)
                return JsonResponse(years,safe=False)
            
            else:
                return JsonResponse({'message':'data not found'},status=204)
        else:
            return JsonResponse({'message':'user is not authenticated'})
    else:
        return JsonResponse({'message':'invalid request method'},status=405)
    
    
def get_subjects(request):
    
    if request.method =='GET':
        
        if request.user.is_authenticated:
            
            id = request.GET.get('mapped_sub')
            year = request.GET.get('year')
            
            subj_data = SubjectMapping.objects.filter(department=id,year=year,deleted_status=False).values('subject_id__subject_name','subject_id__subject_code','id')
            if subj_data:
                return JsonResponse(list(subj_data), safe=False)
            
            else:
                return JsonResponse({'message':'no data found'},status=204)
        else:
            return JsonResponse({'message':'user is not authenticated'})
        
    else:
        return JsonResponse({'message':'invalid request method'},status=405)
    
    
def faculty(request):
    
    if request.method=='GET':
        
        if request.user.is_authenticated:
            
            faculty_data = Faculty.objects.filter(deleted_status=False).values('user_id__first_name','user_id__last_name','title_id__name','id')
            if faculty_data:
                return JsonResponse(list(faculty_data),safe=False)
            
            else:
                return JsonResponse({'message':'data not found'},status=204)
        else:
            return JsonResponse({'message':'user is not authenticated'})
    else:
        return JsonResponse({'message':'invalid request method'},status=405)


def mapped_faculty(request):
    
    if request.method =='GET':
        
        if request.user.is_authenticated:
            
            id = request.GET.get('id')
            faculty_mapping = SubjectTeacherMapping.objects.filter(subject_id =id,deleted_status=False).values('faculty_id__user_id__first_name','faculty_id__user_id__last_name','id')
            if faculty_mapping:
                return JsonResponse(list(faculty_mapping),safe=False)
            
            else:
                return JsonResponse({'message':'data not found'},safe=204)
        else:
            return JsonResponse({'message':'user is not authentiacted'})
    else:
        return JsonResponse({'message':'invalid request method'},status=405)
        
        
            
def admin_chart(request):
    
    if request.method== 'GET':
        
        if request.user.is_authenticated:
            
            id = Dropdown.objects.filter(deleted_status=False,name='Courses').first()
            courses=[]
            departments=[]
            courses= Dropdown.objects.filter(deleted_status=False,relation=id.pk).all()
            print(courses)
            for i in courses:
                id=i['id']
                dept_data=list(Mapping.objects.filter(course = i.id,deleted_status=False).count())
                departments.append(dept_data)
            return JsonResponse(departments,safe=False)
        else:
            return JsonResponse({'message':'user is not authenticated'})
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)




    
  

            
            
            

             
                
                
            
            


    
    