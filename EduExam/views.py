from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import QuestionPaper,PaperResponse,ExamMapping,DateSheet, DateSheetMapping
from EduAdmin.models import UserRole,Dropdown,Mapping,User,Roles,Faculty,Student
from EduCore.models import SubjectMapping,SubjectTeacherMapping,Subject
from EduCore.views import check_user
# from EduExam.models import Subjects
from datetime import datetime, timedelta, date
# import pandas as pd


def questionpaper_validation(load):
    keys_to_check = ['questions', 'exam_type', 'subject', 'department', 'set']
    
    for key in keys_to_check:
        if key not in load:
            return JsonResponse({'message': f'{key} is missing'}, status=400)
          
        value=str(load[key]).strip()
        if value == '':
            return JsonResponse({'message': f'{key} can not be space or none'}, status=400)
        
        elif key == 'exam_type':
            if not value.isdigit():
                return JsonResponse({'message':f'{key} accept only integer'},status=400)
            
        elif key == 'subject':
            if not value.isdigit():
                return JsonResponse({'message':f'{key} accept only integer'},status=400)
            
        elif key == 'department':
            if not value.isdigit():
                return JsonResponse({'message':f'{key} accept only integer'},status=400)
            
        elif key == 'set':
            if not value.isdigit():
                return JsonResponse({'message':f'{key} accept only integer'},status=400)


def question_paper(request):
    
    if request.method=='POST':
        
        if request.user.is_authenticated:
        
            check_faculty = check_user(request.user.id,'Teacher')
            load=json.loads(request.body)
            questions=load.get('questions')
            exam_type=load.get('exam_type')
            subject=load.get('subject')
            department=load.get('department')
            set=load.get('set')
            
            response=questionpaper_validation(load)
            
            if response:
                return response
            
            subject_exist = SubjectMapping.objects.filter(id = subject).first()
            if subject_exist is None:
                return JsonResponse({'messgae':'subject is not found'},status=400)
            
            exam_exist = ExamMapping.objects.filter(exam = exam_type).first()
            if exam_exist is None:
                return JsonResponse({'message':'exam type is not an found'},status=400)
            
            department_exist = Mapping.objects.filter(id = department).first()
            if department_exist is None:
                return JsonResponse({'message':'department is not an found'},status=400)
            
            set_exist = Dropdown.objects.filter(id = set).first()
            if set_exist is None:
                return JsonResponse({'message':'set type is not an found'},status=400)
            
            if check_faculty:
                
                paper,created=QuestionPaper.objects.get_or_create(
                                            exam_type=exam_exist,
                                            subject=subject_exist,
                                            department=department_exist,
                                            set=set_exist,
                                            defaults={"added_by" : check_faculty,"questions":questions}
                                            
                                            )
                if created:
                    return JsonResponse({'message':'Created succesfully'},status=201)
                else:
                    return JsonResponse({'message':'Question peper already created for selected options'},status=409)
            else:
                return JsonResponse({'message':'You are not a Teacher'},status=403)
        else:
            return JsonResponse({'message':'You are not Authenticated'},status=401)
        

    elif request.method=='PUT':
        
        if request.user.is_authenticated:
            
            faculty = check_user(request.user.id, 'Teacher')
            admin = check_user(request.user.id, 'Admin')
            
            load=json.loads(request.body)
            paper_id=load.get('paper_id')
            date=load.get('date')
            question=load.get('questions')
            paper_code=load.get('paper_code')
            start_time=load.get('start_time')
            
            if date is None or question is None or paper_code is None or start_time is None:
                return JsonResponse({'message':'Missing value of any key'},status=400)
            if not date or not question or not paper_code or not start_time:
                return JsonResponse({'message':'Missing Required Field'},status=400)
           
            if faculty or admin:
                
                QuestionPaper.objects.filter(pk=paper_id).update(
                                            paper_code=paper_code,
                                            questions=question,
                                            date=date,
                                            start_time=start_time,
                                            )
                
                return JsonResponse({'message':'Updated Successfully'},status=201)
            else:
                return JsonResponse({'message':'You are not a Teacher or Admin'},status=403)
        else:
            return JsonResponse({'message':'You are not Authenticated'},status=401)
        

    elif request.method == 'DELETE':
        
        if request.user.is_authenticated:
            
            faculty = check_user(request.user.id, 'Teacher')
            admin = check_user(request.user.id, 'Admin')

            paper_id=request.GET.get('papper_id')

            if faculty or admin:
                
                deleted=QuestionPaper.objects.filter(pk=paper_id,deleted_status=False).update(deleted_status=True,deleted_time=datetime.now())
                
                if deleted:
                    return JsonResponse({'message':'Deleted Succesfully'},status=200)
                else:
                    return JsonResponse({'message':'No content'},status=204)
            else:
                return JsonResponse({'message':'You are not autherised'},status=403)
        else:
            return JsonResponse({'message':'You are not logged in'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)


def paper_response(request):
    
    if request.method=='POST':
        if request.user.is_authenticated:
           
            student = check_user(request.user.id, 'Student')

            load = json.loads(request.body)

            answer=load.get('questions')
            paper_id = load.get('paper_id')
            
            if answer is None or paper_id is None :
                return JsonResponse({'message':'Missing value of any key'},status=400)
            if not answer or not paper_id :
                return JsonResponse({'message':'Missing Required Field'},status=400)
            paper_exist = QuestionPaper.objects.filter(id = paper_id).first()
            if paper_exist is None:
                return JsonResponse({'message':'paper is not an Instance'})
            
            if student:
                
                response,created=PaperResponse.objects.get_or_create(
                    paper = paper_exist,
                    added_by = student,
                    defaults={"answer":answer}
                )
                
                if created:
                    return JsonResponse({'message':'Paper successfully submited'},status=201)
                else:
                    return JsonResponse({'message':'You have already submitted this this paper'},status=409)
            else:
                return JsonResponse({'message':'You are not a Teacher'},status=403)
        else:
            return JsonResponse({'message':'You are not Authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)
    

def paper_validation(load):
    
    keys_to_check = ['student_id', 'evaluation', 'marks_obtained']
    
    for key in keys_to_check:
        if key not in load:
            return JsonResponse({'message': f'{key} is missing'}, status=400)  
        
        value=str(load[key]).strip()
        if value == '':
            return JsonResponse({'message': f'{key} can not be space or none'}, status=400)
        
        elif key == 'student_id':
            if not value.isdigit():
                return JsonResponse({'message':f'{key} accept only integer'},status=400)
            
        elif key == 'marks_obtained':
            if not value.isdigit:
                return JsonResponse({'message':f'{key} accept only positive integer'},status=400)

def paper_evaluation(request):
    
    if request.method == 'POST':
        
        if request.user.is_authenticated:
            
            faculty = check_user(request.user.id, 'Teacher')
            print(faculty)
            load=json.loads(request.body)

            student_id=load.get('student_id')
            evaluation=load.get('evaluation')
            marks_obtained=load.get('marks_obtained')

            response=paper_validation(load)
            if response:
                return response


            if faculty:
                evaluated=PaperResponse.objects.filter(added_by=student_id,deleted_status=False,checked_status=False).update(
                evaluation=evaluation,
                checked_status=True,
                checked_time=datetime.now(),
                total_marks=marks_obtained,
                checked_by_id=faculty
                )
                
                if evaluated:
                    return JsonResponse({'message':'Paper checked'},status=200)
                else:
                    return JsonResponse({'message':'You have already checked or deleted this paper'},status=409)
            else:
                return JsonResponse({'message':'You are not autherised'},status=403)
        else:
            return JsonResponse({'message':'You are not logged in'},status=401)
        
    elif request.method == 'PUT':
        
        if request.user.is_authenticated:
            
            faculty = check_user(request.user.id, 'Teacher')


            load=json.loads(request.body)

            paper_id=load.get('paper_id')
            evaluation=load.get('evaluation')

            if faculty:
                
                evaluated=PaperResponse.objects.filter(pk=paper_id,deleted_status=False).update(evaluation=evaluation,checked_time=datetime.now())
                
                if evaluated:
                    return JsonResponse({'message':'Paper edited'})
                else:
                    return JsonResponse({'message':'No content'},status=204)
            else:
                return JsonResponse({'message':'You are not autherised'},status=403)
        else:
            return JsonResponse({'message':'You are not logged in'},status=401)
        
    elif request.method == 'DELETE':
        
        if request.user.is_authenticated:
            
            faculty = check_user(request.user.id, 'Teacher')
            paper_id=request.GET.get('papper_id')

            if faculty:
                
                deleted=QuestionPaper.objects.filter(pk=paper_id,deleted_status=False).update(deleted_status=True,deleted_time=datetime.now())
                
                if deleted:
                    return JsonResponse({'message':'Deleted Succesfully'})
                else:
                    return JsonResponse({'message':'No content'},status=204)
            else:
                return JsonResponse({'message':'You are not autherised'},status=403)
        else:
            return JsonResponse({'message':'You are not logged in'},status=401)
    
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)

def get_student_response(request):
    
    if request.method=='GET':
        
        if request.user.is_authenticated:
            
            faculty = check_user(request.user.id, 'Teacher')

            if faculty:
                
                data=PaperResponse.objects.filter(deleted_status=False).values('added_by','added_by__first_name','added_by__last_name','paper__exam_type__exam__name')
                
                if data:
                    return JsonResponse(list(data),safe=False)
                else:
                    return JsonResponse({'message':'No content'},status=204)
            else:
                return JsonResponse({'message':'You are not autherised'},status=403) 
        else:
            return JsonResponse({'message':'You are not authenticated'},status=401) 
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405) 


def get_question_answer(request):
    
    if request.method=='GET':
        
        if request.user.is_authenticated:
            
            faculty = check_user(request.user.id, 'Teacher')
            subject_id=request.GET.get('subject_id')
            faculty_subject=SubjectTeacherMapping.objects.filter(faculty=request.user.id,subject=subject_id).first()
                        
            if faculty:
                student_id=request.GET.get('student_id')
                
                if student_id is None:
                    return JsonResponse({'message':'You are not sending student id'},status=400)

                data=PaperResponse.objects.filter(added_by=student_id,deleted_status=False).values('added_by','answer')
                if data:
                    return JsonResponse(list(data),safe=False)
                else:
                    return JsonResponse({'message':'Data not found'},status=204)
            else:
                return JsonResponse({'message':'You are not autherised'},status=403) 
        else:
            return JsonResponse({'message':'You are not authenticated'},status=401) 
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405) 
    
def paper_sets(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            faculty = check_user(request.user.id,'Teacher')
            if faculty:

                dept_id=request.GET.get('dept_id')
                sub_id=request.GET.get('sub_id')
                exam_id=request.GET.get('exam_id')

                if not sub_id or sub_id is None:
                    return JsonResponse({'message':'sub id missing or none'},status=400)

                if not exam_id or exam_id is None:
                    return JsonResponse({'message':'exam id missing or none'},status=400)

                if not dept_id or dept_id is None:
                    return JsonResponse({'message':'dept id missing or none'},status=400)

                subject_exist = SubjectMapping.objects.filter(id = sub_id).first()
                if subject_exist is None or not sub_id:
                    return JsonResponse({'messgae':'subject is not found'},status=400)

                department_exist = Mapping.objects.filter(id = dept_id).first()
                if department_exist is None or not dept_id:
                    return JsonResponse({'message':'department is not an found'},status=400)

                exam_exist=ExamMapping.objects.filter(exam=exam_id).first()
                if exam_exist is None or not exam_exist:
                    return JsonResponse({'message':'exama is not found'},status=400)

                data=QuestionPaper.objects.filter(deleted_status=False,department=dept_id,subject=sub_id,exam_type=exam_exist).values('pk','added_by','set__name')
                if data:
                    return JsonResponse(list(data),safe=False)
                else:
                    return JsonResponse({'message':'No answers found'},status=204)
            else:
                return JsonResponse({'message':'user is not faculty'},status=403)
        else:
            return JsonResponse({"message":'user is not authentiacted'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)


def get_students_answer(request):
    
    if request.method== 'GET':
        
        if request.user.is_authenticated:
            
            faculty = check_user(request.user.id, 'Teacher')
            if faculty:
                paper_id=request.GET.get('paper_id')
                
                if paper_id is None or not paper_id:
                    return JsonResponse({'message':'Paper id is required'},status=400)
                
                data=PaperResponse.objects.filter(deleted_status=False,paper=paper_id).values('added_by','added_by__first_name','added_by__last_name','checked_status')
                if data:
                    return JsonResponse(list(data),safe=False)
                
                else:
                    return JsonResponse({'message':'No answers found'},status=204)
            else:
                return JsonResponse({'message':'user is not faculty'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)




def exam_mapping(request):
    
        if request.user.is_authenticated:
            
            admin = check_user(request.user.id, 'Admin')
            
            if request.method =='POST':
                load = json.loads(request.body)
                exam_type = load.get('exam_type_id')
                duration=load.get('duration')
                marks = load.get('marks')
                
                if duration is None or marks is None or exam_type is None :
                    return JsonResponse({'message':'Missing value of any key'},status=400)
                
                if not duration or not marks or not exam_type :
                    return JsonResponse({'message':'Missing Required Field'},status=400)
                
                exam_exist = Dropdown.objects.filter(pk = exam_type).first()
                if exam_exist is None:
                    return JsonResponse({'message':'Given data do not match with Existing Query'},status=400)
                
                duration_exist = Dropdown.objects.filter(pk = duration).first()
                if duration_exist is None:
                    return JsonResponse({'messgae':'Given data do not match with Existing Query'},status=400)
                
                marks_exist = Dropdown.objects.filter(pk = marks).first()
                if marks_exist is None:
                    return JsonResponse({'message':'Given data do not match with Existing Query'},status=400)
                
                if admin:
                    mapping, created = ExamMapping.objects.get_or_create(
                        duration=duration_exist,
                        exam=exam_exist,
                    marks=marks_exist,
                    defaults={"added_by":admin}

                    )
                    
                    if created:
                        return JsonResponse({'message':'Exam Mapping successfully done'})
                    else:
                        return JsonResponse({'message':'Mapping already exist'},status=409)
                else:
                    return JsonResponse({'message':'admin not found'},status=204)
            elif request.method=='PUT':
                
                load = json.loads(request.body)
                id = load.get('id')
                marks_id = load.get('marks')
                duration_id = load.get('duration')
                
                marks_exist = Dropdown.objects.filter(id = marks_id).first()
                if marks_exist is None:
                    return JsonResponse({'message':'data not found'},status=204)
                
                duration_exist = Dropdown.objects.filter(id = duration_id).first()
                if duration_exist is None:
                    return JsonResponse({'message':'data not found'},status=204)
                
                ExamMapping.objects.filter(id = id).update(marks=marks_exist,duration=duration_exist)
                return JsonResponse({'message':'successfully updated'})
            
            elif request.method=='DELETE':
                
                 id = request.GET.get('id')
                 
                 id_exist = ExamMapping.objects.filter(id = id).first()
                 if id_exist:
                     ExamMapping.objects.filter(id = id).update(deleted_status=True, deleted_time=datetime.now())
                     return JsonResponse({'message':'successfully deleted'})
                 
                 else:
                     return JsonResponse({'message':'data not found'},status=204)                   
            else:
                return JsonResponse({'message':'invalid request method'},status=405)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=403)


def department_course(request):
    
    if request.method == 'GET':
        
        if request.user.is_authenticated:
            
            id=Faculty.objects.filter(user=request.user.id).first()
            if not id :
                return JsonResponse({'message':'You not have any department'},status=400)
            
            data=SubjectTeacherMapping.objects.filter(deleted_status=False,faculty=id).values('subject__department__course','subject__department__pk','subject__department__department__name','subject__department__course__name').distinct()
            if data:
                return JsonResponse(list(data),safe=False)
            
            else:
                return JsonResponse({'message':'No Content'},status=204)
        else:
            return JsonResponse({'message':'user is not authentiacted'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)
            
def subject_year(request):
    
    if request.method == 'GET':
        
        if request.user.is_authenticated:
            faculty=check_user(request.user.id,'Teacher')
            if faculty:
                department_id=request.GET.get('dept_id')
                subject_id=[]
                subjects=[]
                id=Faculty.objects.filter(deleted_status=False,user=request.user.id).first()
                data=SubjectTeacherMapping.objects.filter(deleted_status=False,faculty=id).values('subject')
                for i in data:
                    subject_id.append(i['subject'])
                for i in subject_id:
                    sub=list(SubjectMapping.objects.filter(pk=i,department=department_id).values('pk','year','subject__subject_name','subject__subject_code'))
                    if sub:
                        subjects.append(sub)
                if subjects != []:
                    return JsonResponse(subjects,safe=False)
                
                else:
                   return JsonResponse({'message':'No Content'},status=204)
        else:
            return JsonResponse({"message":'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)  



def exam_type(request):
    
    if request.method == 'GET':
        
        if request.user.is_authenticated:
            
            id=Dropdown.objects.filter(deleted_status=False,name='Exam Type').first()
            if id is None:
                return JsonResponse({'message':'Exam Type not match'},status=400)
            
            exam_type=Dropdown.objects.filter(deleted_status=False,relation=id).values('pk','name')
            if exam_type:
                return JsonResponse(list(exam_type),safe=False)
            
            else:
                return JsonResponse({'message':'No Content'},status=204)
        else:
            return JsonResponse({"message":'user is not authenticated'})
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)

def exam_info(request):
    
    if request.method == 'GET':
        
        if request.user.is_authenticated:
            
            id=request.GET.get('id')
            if id is None or not id:
                return JsonResponse({'message':'You are not sending exam id'},status=400)
            # data=DateSheetMapping.objects.filter(deleted_status=False,year=1,exam_mapping=3, )
            data=ExamMapping.objects.filter(deleted_status=False,exam=id).values('marks__name','duration__name')
            if data:
                return JsonResponse(list(data),safe=False)
            
            else:
                return JsonResponse({'message':'No Content'},status=204)
        else:
            return JsonResponse({"message":'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)         
            


def access_question(request):
    
    if request.method=='GET':
        
        if request.user.is_authenticated:
            
            student=Student.objects.filter(user=request.user.id).first()
            if student is None:
                return JsonResponse({'message':'You have not filled your data'},status=400)
            
            data=SubjectMapping.objects.filter(department=student.department,year=student.year,deleted_status=False).values('pk','subject__subject_name').distinct()
            if data:
                return JsonResponse(list(data),safe=False)
            
            else:
                return JsonResponse({'message':'No content'},status=204)
        else:
            return JsonResponse({"message":'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)     


def select_paper_set(request):
    
    if request.method == 'GET':
        
        if request.user.is_authenticated:
        
            sub_id=request.GET.get('sub_id')
            exam_id=request.GET.get('exam_id')

            if not sub_id or sub_id is None:
                return JsonResponse({'message':'sub id missing or none'},status=400)
            
            if not exam_id or exam_id is None:
                return JsonResponse({'message':'exam id missing or none'},status=400)

            subject_exist = SubjectMapping.objects.filter(id = sub_id).first()
            if subject_exist is None or not sub_id:
                return JsonResponse({'messgae':'subject is not found'},status=400)

            student=Student.objects.filter(user=request.user.id).first()
            if student is None :
                return JsonResponse({'message':'student data not found'},status=400)

            exam_exist=ExamMapping.objects.filter(exam=exam_id).first()
            if exam_exist is None or not exam_exist:
                return JsonResponse({'message':'exama is not found'},status=400)

            data=QuestionPaper.objects.filter(deleted_status=False,department=student.department,subject=sub_id,exam_type=exam_exist).values('pk','added_by','set__name')
            if data:
                return JsonResponse(list(data),safe=False)
            
            else:
                return JsonResponse({'message':'No answers found'},status=204)
        else:
            return JsonResponse({'message':'user is not authentiacted'}, status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)

def get_question_paper(request):
    
    if request.method=='GET':
        
        if request.user.is_authenticated:
            
            student = check_user(request.user.id, 'Student')
            if student:
                
                paper_id=request.GET.get('paper_id')
                if paper_id is None or not paper_id:
                    return JsonResponse({'message':'Paper id is required'},status=400)
                
                if PaperResponse.objects.filter(added_by=student.id,paper=paper_id).exists():
                    return JsonResponse({'message':'You already submited this paper'},status=200)
                
                data=QuestionPaper.objects.filter(deleted_status=False,pk=paper_id).values('pk','questions','exam_type__duration__name')
                if data:
                    return JsonResponse(list(data),safe=False)
                
                else:
                    return JsonResponse({'message':'Paper not found'},status=204)
            else:
                return JsonResponse({'message':'You are not a student'},status=403)
        else:
            return JsonResponse({'message':'You are not authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)
    

def view_paper(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            faculty=check_user(request.user.id, 'Teacher')
            if faculty:
                data=QuestionPaper.objects.filter(deleted_status=False,added_by=request.user.id).values('pk','set__name','exam_type__exam__name','department__course__name','department__department__name','subject__year','subject__subject__subject_name','subject__subject__subject_code')
                if data:
                    return JsonResponse(list(data),safe=False)
                else:
                    return JsonResponse({'message':'No paper found'},status=204)
            else:
                return JsonResponse({'message':'You are not faculty'},status=403)
        else:
            return JsonResponse({'message':'You are not logged in'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)
    




def datesheet_validation(load):
    
    keys_to_check = ['subject', 'exam_map', 'shift', 'date', 'start_time']
    
    for key in keys_to_check:
        if key not in load:
            return JsonResponse({'message': f'{key} is missing'}, status=400)  
        
        value=str(load[key]).strip()
        if value=='':
            return JsonResponse({'message': f'{key} can not be space or none'}, status=400)

def datesheet_maping(request):
    
    if request.user.is_authenticated:
        admin = check_user(request.user.id, 'Admin')

        if admin:
            if request.method == 'POST':

                load=json.loads(request.body)
                load_data = datesheet_validation(load)
                if load_data:
                    return load_data
                
                else:
                    subject=load.get('subject')
                    exam_map=load.get('exam_map')
                    shift=load.get('shift')
                    date=load.get('date')
                    start_time=load.get('start_time')
                    
                    exam_exist=ExamMapping.objects.filter(pk=exam_map,deleted_status=False).first()
                    if exam_exist is None:
                        return JsonResponse({'message':'Exam_mapping is not an instance'},status=400)
                    
                    subject_exist=SubjectMapping.objects.filter(pk=subject,deleted_status=False).first()
                    if subject_exist is None:
                        return JsonResponse({'message':'Subject is not an instance'},status=400)
                    
                    shift_exist=Dropdown.objects.filter(pk=shift,deleted_status=False).first()
                    if shift_exist is None:
                        return JsonResponse({'message':'Shift is not an instance'},status=400)
                    
                    datesheet,created=DateSheet.objects.get_or_create(subject=subject_exist,
                    exam_mapping=exam_exist,
                    shift=shift_exist,
                    date=date,
                    start_time=start_time,
                    defaults={"added_by":admin}
                    )
                    
                    if created:
                        return JsonResponse({'message':'Exam mapped succesfully'},status=201)
                    
                    else:
                        return JsonResponse({'message':'Exam mapping already exist'},status=409)
                
            elif request.method == 'PUT':
                load=json.loads(request.body)
        
                datesheet_it=load.get('id')
                shift=load.get('shift')
                date=load.get('date')
                start_time=load.get('start_time')
    
                if datesheet_it is None or shift is None or date is None or start_time:
                    return JsonResponse({'message':'Missing any key'},status=400)
                
                if datesheet_it or not shift or not date or not start_time:
                    return JsonResponse({'message':'Missing required field'},status=400)
                
                datesheet_exist=DateSheet.objects.filter(pk=exam_map).first()
                if exam_exist is None:
                    return JsonResponse({'message':'Datesheet is not an instance'},status=400)
                
                shift_exist=Dropdown.objects.filter(pk=shift).first()
                if shift_exist is None:
                    return JsonResponse({'message':'Shift is not an instance'},status=400)
                
                updated=DateSheet.objects.filter(pk=datesheet_exist.pk).update(
                shift=shift_exist.pk,
                date=date,
                start_time=start_time,
                )

                if updated:
                    return JsonResponse({'message':'Updated succesfuly'},status=200)
                else:
                    return JsonResponse({'message':'Datesheet not found'},status=400)
                
            elif request.method == 'DELETE':
                
                datesheet_it=request.GET.get('id')
                if datesheet_it is None:
                    return JsonResponse({'message':'You are not sending datesheet id'},status=400)
                
                deleted=DateSheet.objects.filter(pk=datesheet_it,deleted_status=False).update(deleted_status=True,deleted_time=datetime.now())
                if deleted:
                    return JsonResponse({'message':'Deleted succesfully'},status=200)
                
                else:
                    return JsonResponse({'message':'Datesheet not found'},status=400)
            else:
                return JsonResponse({'message':'Invalid Request Method'},status=405)
        else:
            return JsonResponse({'message':'You are not autherised'},status=403)
    else:
        return JsonResponse({'message':'You are not logged in'},status=401)

def course_dept_mapping(request):
    
    if request.method =='GET':
        
        if request.user.is_authenticated:
            
            all_mapping_data = Mapping.objects.filter(deleted_status=False).values('id','course_id__name','department_id__name')
            if all_mapping_data:
                return JsonResponse(list(all_mapping_data), safe=False)
            
            else:
                return JsonResponse({'message':'data not found'},status=204)
        else:
            return JsonResponse({"message":'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'invalid request method'}, status=405)

def all_exam_mapping(request):
    
    if request.method =='GET':
        
        if request.user.is_authenticated:
            
            all_data = ExamMapping.objects.filter(deleted_status=False).values('id','duration_id__name','exam_id__name','marks_id__name')
            if all_data:
                return JsonResponse(list(all_data), safe=False)
            
            else:
                return JsonResponse({'message':'user is not authentiacted'})
        else:
            return JsonResponse({'message':'user is not authenticated'})
    else:
        return JsonResponse({'messgae':'invalid request method'},status=405)      
def conduct_datesheet(request):
    
    if request.method=='POST':
        
        if request.user.is_authenticated:
            
            admin = check_user(request.user.id, 'Admin')
            if admin:
                
                load = json.loads(request.body)
                exam_mapping_id = load.get('exam_mapping_id')
                course_id = load.get('course_dept_id')
                year = load.get('year')
                start_date = load.get('start_date')
                end_date = load.get('end_date') 
                
                if exam_mapping_id is None or course_id is None or year is None or start_date is None or end_date is None:
                    return JsonResponse({'message':'missing any key'}, status=400)
                
                if not exam_mapping_id or not course_id or not year or not start_date or not end_date:
                    return JsonResponse({'message':'Missing Required Field'},status=400)
                
                exam_exist = ExamMapping.objects.filter(id = exam_mapping_id).first()
                if exam_exist is None:
                    return JsonResponse({'messgae':'existing query do not match, data not found'}, status=204)
                
                course_exist = Dropdown.objects.filter(id = course_id).first()
                if course_exist is None:
                    return JsonResponse({'message':'existing query do not match, data not found'}, status=204)
                
                datesheet_mapping, created = DateSheetMapping.objects.get_or_create(
                    exam_mapping = exam_exist,
                    course_id=course_exist.pk,
                    year=year,
                    start_date=start_date,
                    end_date=end_date,
                    defaults={'added_by':admin}
                    
                )
                
                if created:
                    return JsonResponse({'message':'Successfully Conduct Examination '})
                
                else:
                    return JsonResponse({'message':'Existing Query already present'}, status=409)
            else:
                return JsonResponse({'message':'user is not admin'}, status=401)
        else:
            return JsonResponse({'message':'user is not authenticated'}, status=403)
    else:
        return JsonResponse({'message':'invalid request method'}, status=405)

def get_exam_mapping(request):
    
    if request.method=='GET':
        
        if request.user.is_authenticated:
            
            datesheet_mapping_data = DateSheetMapping.objects.filter(deleted_status=False, start_date__gte=date.today()).values('id','year','start_date','end_date','course_id__name','exam_mapping__duration_id__name','exam_mapping__exam_id__name','exam_mapping__marks_id__name','course_id__id')
            if datesheet_mapping_data:
                return JsonResponse(list(datesheet_mapping_data), safe=False)
            
            else:
                return JsonResponse({'message':'data not found'},status=401)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'invalid request method'}, status=405)
    
def selectdept(request):
    
    if request.method=='GET':
        
        if request.user.is_authenticated:
            
            course_id = request.GET.get('id')
            
            department_data = Mapping.objects.filter(course_id = course_id).values('id','department_id__name','course_id')
            if department_data:
                return JsonResponse(list(department_data), safe=False)
            
            else:
                return JsonResponse({'message':'data not found'},status=204)
        else:
            return JsonResponse({'message':'user is not authentiacted'},status=401)
    else:
        return JsonResponse({'message':'invalid request method'},status=405)

def select_sub(request):
    
    if request.method =='GET':
        
        if request.user.is_authenticated:
            
             check_Admin=check_user(request.user.id, 'Admin')
             if check_Admin:
                
                 id = request.GET.get('id')
                 year = request.GET.get('year')
                 id_data = id.split(',')
                 length = len(id_data)
                 
                 if id: 
                     dept = []
                     datesheet_details=[]
                     datesheet_data=[]
                     sub_data=[]
                     
                     for i in range(length):
                         print(id_data[i])
                         dept.append(id_data[i])
                         
                     for i in dept:
                         subject_data = list(Mapping.objects.filter(course_id =int(i), deleted_status=False).values('id'))
                         datesheet_details.append(subject_data)
                         
                     for sublist in datesheet_details:
                       for item in sublist:
                         for dictionary in item:
                             datesheet_data.append(item[dictionary])
                             
                     for i in datesheet_data:
                              sub_details =SubjectMapping.objects.filter(department_id=int(i), year=year,deleted_status=False).values('subject_id__subject_name','subject_id__id','department_id__department_id__name','department_id').distinct()
                              sub_data.append(list(sub_details))
                     return JsonResponse(list(sub_data), safe=False)
                 
                 else:
                    return JsonResponse({'message':'data not found'},status=204)
             else:
                 return JsonResponse({'message':'user is not Admin'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated'}, status=401)
    else:
        return JsonResponse({'messsage':'invalid method request'},status=405)
                                                         
def show_exam_type(request):
    
    if request.method =='GET':
        if request.user.is_authenticated:
        
            exam_mapping_data = ExamMapping.objects.filter(deleted_status=False).values('id','duration_id__name','exam_id__name','marks_id__name')
            if exam_mapping_data:
                return JsonResponse(list(exam_mapping_data), safe=False)
            
            else:
                return JsonResponse({'message':'data not found'}, status=204)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'invalid request method'}, status=405)
    
def get_date(request):
    
    if request.method =='GET':
        if request.user.is_authenticated:
        
            id = request.GET.get("id")
            get_dates= DateSheetMapping.objects.filter(id = id).first()
            start_date = get_dates.start_date
            end_date=get_dates.end_date
            
            get_date_btw =get_dates_between(start_date,end_date)
            if get_date_btw:
                return JsonResponse(list(get_date_btw), safe=False)
            
            else:
                return JsonResponse({'message':'date not found'},status=204)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'invalid request method'},status=405)
        

def get_dates_between(start_date, end_date):
    
    dates = [start_date + timedelta(n) for n in range(int((end_date - start_date).days)) if (start_date+timedelta(n)).weekday()!=6]
    return dates

def get_shift_time(request):
    
    if request.method=='GET':
        if request.user.is_authenticated:
        
            id = request.GET.get("id")
            get_shift_data = Dropdown.objects.filter(relation_id = id).values("name",'id')

            if get_shift_data:

                return JsonResponse(list(get_shift_data), safe=False)
            else:
                return JsonResponse({'message':'data not found'},status=204)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'invalid request method'},status=405)
        

def datesheet(request):
    
    if request.method=='POST':
        
        if request.user.is_authenticated:
            
            admin = check_user(request.user.id, 'Admin')
            
            if admin:
                load = json.loads(request.body)
                conduct_exam_id = load.get('course_id')
                subject = load.get('subject')
                date = load.get('date')
                shift= load.get('shift')
                time = load.get('time')
                course_dept = load.get('mapping_id')
                
                exam_published= DateSheetMapping.objects.filter(id = conduct_exam_id,published='1').first()
                if exam_published :
                    return JsonResponse({'message':'This is already Published'},status=409)
                
                exam_exist = DateSheetMapping.objects.filter(id = conduct_exam_id).first()
                if exam_exist is None:
                    return JsonResponse({'message':'examtype not found'},status=204)
                
                subject_exist = Subject.objects.filter(id = subject).first()
                if subject_exist is None:
                    return JsonResponse({'message':'subject found'}, status=204)
                
                shift_exist = Dropdown.objects.filter(id = shift).first() 
                if shift_exist is None:
                    return JsonResponse({'message':'shift not found'},status=204)
                
                start_time_exist = Dropdown.objects.filter(id = time).first()
                if start_time_exist is None:
                    return JsonResponse({'message':'start time not found'},status=204)
                
                mapping_exist = Mapping.objects.filter(id = course_dept).first()
                if mapping_exist is None:
                    return JsonResponse({'message':'course/dept not found'},status=204)
                
                subject_mapped = DateSheet.objects.filter(datesheet_mapping_id = conduct_exam_id,course_department_id = course_dept,subject_id = subject).first()
                print(subject_mapped)
                if subject_mapped:
                    return JsonResponse({"message":f"{subject_mapped.subject.subject_name} EXAM is already added for {subject_mapped.date}"},status=409)
                department_date_mapped = DateSheet.objects.filter(course_department_id = course_dept,date = date,shift_id = shift).first()
                if department_date_mapped:
                    return JsonResponse({'message':f'{department_date_mapped.subject.subject_name} EXAM is already conduct on {department_date_mapped.date} for {department_date_mapped.course_department.department.name} department'},status=409)
                
                
                datesheet, created=DateSheet.objects.get_or_create(
                    date=date,
                    start_time=start_time_exist,
                    course_department=mapping_exist,
                    defaults={'added_by': admin,"datesheet_mapping":exam_exist,
                    "subject" : subject_exist, "shift":shift_exist,}
                )   
                if created: 
                    
                    return JsonResponse({'message':'added successfully'}, status=201)
                else:
                    return JsonResponse({'message':'already created'},status=409)
            else:
                return JsonResponse({'message':'user is not admin'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'invalid request method'},status=405)

def graph_course_dept(request):
    
     if request.method == 'GET':
         
        if request.user.is_authenticated:
            
            admin = check_user(request.user.id,'Admin')
            faculty = check_user(request.user.id,'Teacher')
            student = check_user(request.user.id,'Student')
            
            if admin:
                
                courses = Dropdown.objects.filter(relation_id='2').all()
                data = {
                    'course_name':[],
                    'department_count':[]
                }   

                for course_id in courses:
                    department_count = Mapping.objects.filter(course_id=course_id.id).count()
                    data['course_name'].append(course_id.name)
                    data['department_count'].append(department_count)
                return JsonResponse(data, safe=False)
            
            elif faculty:
                courses = Dropdown.objects.filter(relation_id='2').all()
                data = {
                    'course_name':[],
                    'department_count':[]
                }   

                for course_id in courses:
                    print(course_id.id)
                    department_count = Mapping.objects.filter(course_id=course_id.id).count()
                    data['course_name'].append(course_id.name)
                    data['department_count'].append(department_count)
                return JsonResponse(data, safe=False)
             
            elif student:
                courses = Dropdown.objects.filter(relation_id='2').all()
                data = {
                    'course_name':[],
                    'department_count':[]
                }   

                for course_id in courses:
                    print(course_id.id)
                    department_count = Mapping.objects.filter(course_id=course_id.id).count()
                    data['course_name'].append(course_id.name)
                    data['department_count'].append(department_count)
                return JsonResponse(data, safe=False)
             
            else:
                return JsonResponse({'user not found'},status=400)
        else:
            return JsonResponse({'message': 'User is not authenticated'}, status=401)
     else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

    
def subject_mapped_dept(request):
    
    if request.method=='GET':
        
        if request.user.is_authenticated:
            
            year = request.GET.get('year')
            subject_id = request.GET.get('subject')
            
            departments = SubjectMapping.objects.filter(year=year,subject_id=subject_id).values('department_id__department_id__name','department_id','department_id__course_id__name').distinct()
            if departments:

                return JsonResponse(list(departments),safe=False)
            else:
                return JsonResponse({'message':'data not found'},status=204)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'invalid request method'}, status=405)
def subjects(request):
    
    if request.method =='GET':
        
        if request.user.is_authenticated:
            
            student = check_user(request.user.id,'Student')
            if student:
                
                paper = []
                response = []
                exam_type_id = request.GET.get('exam_id')
                
                exam_exist = QuestionPaper.objects.filter(exam_type_id=exam_type_id).values('id','subject_id__subject_id__subject_name')
                for exam in exam_exist:
                    paper.append(exam['id'])
                    
                for i in paper:
                    student_mark=PaperResponse.objects.filter(added_by = request.user.id, paper_id=i).values('total_marks','paper_id__subject_id__subject_id__subject_name','paper_id__subject_id__subject_id__subject_code','paper_id__exam_type_id__exam_id__name','paper_id__exam_type_id__marks_id__name')
                    response.append(list(student_mark))
                    
                    if student_mark:
                        return JsonResponse(list(response), safe=False)
                    
                else:
                    return JsonResponse({'message':'data not found'},status=204)
            else:
                return JsonResponse({'message':'not student logged in'}, status=403)
        else:
            return JsonResponse({"message":'user is not authenticated'}, status=401)
    else:
        return JsonResponse({'message':'invalid request method'}, status=405)
    

def student_marks(request):
    if request.method =='GET':
        # year = request.GET.get('year')
        # course_id = request.GET.get('id')
        # SubjectMapping.objects.filter(year = year, department_id = course_id)

        if request.user.is_authenticated:
            student = check_user(request.user.id,'Student')
            if student:
                paper = []
                response = []
                exam_type_id = request.GET.get('exam_id')

                exam_exist = QuestionPaper.objects.filter(exam_type_id=exam_type_id).values('id','subject_id__subject_id__subject_name')
                for exam in exam_exist:
                    print(exam['id'])
                    paper.append(exam['id'])
                print(paper)
                for i in paper:
                    print(i)
                    student_mark=PaperResponse.objects.filter(added_by = request.user.id, paper_id=i).values('total_marks','paper_id__subject_id__subject_id__subject_name','paper_id__subject_id__subject_id__subject_code','paper_id__exam_type_id__exam_id__name','paper_id__exam_type_id__marks_id__name')
                    response.append(list(student_mark))
                    if student_mark:
                        return JsonResponse(list(response), safe=False)
                else:
                    return JsonResponse({'message':'data not found'},status=204)
            else:
                return JsonResponse({'message':'not student logged in'}, status=403)
        else:
            return JsonResponse({"message":'user is not authenticated'}, status=401)
    else:
        return JsonResponse({'message':'invalid request method'}, status=405)



def exam_type_for_marks(request):
    
    if request.method =='GET':
        
        
        if request.user.is_authenticated:
            student =check_user(request.user.id,'Student')
            
            if student:
            
                exams = QuestionPaper.objects.filter(deleted_status=False).values('exam_type_id','exam_type_id__exam_id__name','exam_type_id__marks_id__name').distinct()
                if exams:
                    return JsonResponse(list(exams), safe=False)

                else:
                    return JsonResponse({'message':'data not found'}, status=204)
            else:
                return JsonResponse({'message':'user is not student'},status=401)
        else:
            return JsonResponse({'message':'user is not authentiacted'},status=401)
    else:
        return JsonResponse({'message':'invalid request method'},status=405)
    
def get_datesheet(request):
    
    if request.method=='GET':
        
        if request.user.is_authenticated:
            admin = check_user(request.user.id,'Admin')
            if admin:
            
                id = request.GET.get('id')
                if id :

                    datesheet_data = DateSheet.objects.filter(datesheet_mapping_id=id,deleted_status=False).values('date','course_department_id__department_id__name','subject_id__subject_name','subject_id__subject_code','shift_id__name','start_time__name')
                    if datesheet_data:
                        return JsonResponse(list(datesheet_data),safe=False)

                    else:
                        return JsonResponse({'message':'no content found'},status=204)
                else:
                    return JsonResponse({'message':'no content found'},status=204)
            else:
                return JsonResponse({"message":'user is not admin'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'invalid request method'},status=405)
    
def publish_datesheet(request):
    
    if request.method =='POST':
        
        if request.user.is_authenticated:
            
            admin=check_user(request.user.id,'Admin')
            if admin:
                
                load = json.loads(request.body)
                id = load.get('id')
                check_datesheet = DateSheetMapping.objects.filter(id = id).first()
                print(check_datesheet.year)
                if check_datesheet:
                    
                    year = check_datesheet.year
                    department=[]
                    subject=[]
                    
                    check_departments = DateSheet.objects.filter(datesheet_mapping_id = id).values('course_department_id').distinct()
                    for i in check_departments:
                        department.append(i['course_department_id'])
                        
                    for i in department:
                        check_subjects = SubjectMapping.objects.filter(department_id=i, year= year).values('subject_id__id')
                        
                        for i in check_subjects:
                            subject.append(i['subject_id__id'])
                            
                    for i in subject:
                        check_all_subject_presence = DateSheet.objects.filter(datesheet_mapping_id = id,subject_id = i).exists()
                        if check_all_subject_presence is False:
                            return JsonResponse({"message": "Please add all subject corresponding to choosen department"},status=100)
                    DateSheetMapping.objects.filter(id = id).update(published = True, published_time = datetime.now())
                    return JsonResponse({'message':f'Datesheet successfully Published for conducting {check_datesheet.exam_mapping.exam.name}'})
                
                else:
                    return JsonResponse({'message':'data not found'},status=204)
            else:
                return JsonResponse({'message':'user is not Admin'},status=403)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=401)
    else:
        return JsonResponse({'message':'invalid request method'},status=405)
def student_marks(request):
    if request.method =='GET':
        print(request)
        
        if request.user.is_authenticated:
            
            student = check_user(request.user.id,'Student')
            if student:
                paper = []
                response = []
                exam_type_id = request.GET.get('exam_id')
                exam_exist = QuestionPaper.objects.filter(exam_type_id=exam_type_id).values('id','subject_id__subject_id__subject_name')
                
                for exam in exam_exist:
                    paper.append(exam['id'])
                    
                for i in paper:
                    student_mark=PaperResponse.objects.filter(added_by = request.user.id, paper_id=i).values('total_marks','paper_id__subject_id__subject_id__subject_name','paper_id__subject_id__subject_id__subject_code','paper_id__exam_type_id__exam_id__name','paper_id__exam_type_id__marks_id__name')
                    response.append(list(student_mark))
                    
                    if student_mark:
                        return JsonResponse(list(response), safe=False)
                    
                else:
                    return JsonResponse({'message':'data not found'},status=204)
            else:
                return JsonResponse({'message':'not student logged in'}, status=403)
        else:
            return JsonResponse({"message":'user is not authenticated'}, status=401)
    else:
        return JsonResponse({'message':'invalid request method'}, status=405)

def show_examtype_to_student(request):
    
    if request.method =='GET':
        
        if request.user.is_authenticated:
            
            student = check_user(request.user.id,'Student')
            if student:
                student_data = Student.objects.filter(user=student).first()
                exam_type_exist = DateSheetMapping.objects.filter(published=True,deleted_status=False,year=student_data.year,course_id = student_data.course.id).first()
                
                if exam_type_exist:
                    exam_data = DateSheetMapping.objects.filter(published=True,deleted_status=False,year=student_data.year,course_id = student_data.course.id).values('id','exam_mapping_id__exam_id__name','exam_mapping_id__duration_id__name','exam_mapping_id__marks_id__name')
                    return JsonResponse(list(exam_data),safe=False)
                
                else:
                    return JsonResponse({'message':'No Exam Found'})
            else:
                    return JsonResponse({'message':'User is not Student'},status=403)
        else:
            return JsonResponse({"message":'User is not authenticated'}, status=401)
    else:
        return JsonResponse({'message':'Invalid request method'}, status=405)
    
def show_datesheet(request):
    if request.method=='GET':
        
         if request.user.is_authenticated:
             
              student = check_user(request.user.id,'Student')
              if student:
                  
                  id = request.GET.get('id')
                  datesheet_exist = DateSheet.objects.filter(datesheet_mapping_id=id,deleted_status=False).first()
                  if datesheet_exist:
                      datesheet_data=DateSheet.objects.filter(datesheet_mapping_id=id,deleted_status=False).values('id','shift_id__name','date','subject_id__subject_name','subject_id__subject_code','start_time_id__name')
                      return JsonResponse(list(datesheet_data),safe=False)
                  
                  else:
                      return JsonResponse({'message':'Datesheet not Found'},status=204)
              else:
                  return JsonResponse({'message':'User is not Student'},status=403)
         else:
            return JsonResponse({"message":'User is not authenticated'}, status=401)
    else:
        return JsonResponse({'message':'Invalid request method'}, status=405)
         
                      
             
                       
                        
                    
                   
                

            
                

    


    