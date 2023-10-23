from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import QuestionPaper,PaperResponse,ExamMapping,DateSheet
from EduAdmin.models import UserRole,Dropdown,Mapping,User,Roles,Faculty,Student
from EduCore.models import SubjectMapping,SubjectTeacherMapping
# from EduExam.models import Subjects
from datetime import datetime,date


def question_paper(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            id=Roles.objects.get(role_name='Teacher',deleted_status=False)
            faculty_exist=UserRole.objects.filter(user=request.user.id,role_id = id.pk).first()
            load=json.loads(request.body)
            # date=load.get('date')
            questions=load.get('questions')
            exam_type=load.get('exam_type')
            subject=load.get('subject')
            # paper_code=load.get('paper_code')
            department=load.get('department')

          

            if  exam_type is None or subject is None or department is None or questions is None:
                return JsonResponse({'message':'Missing value of any key'},status=400)
            if not subject or not questions or not exam_type or not  department:
                return JsonResponse({'message':'Missing Required Field'},status=400)
            subject_exist = SubjectMapping.objects.filter(id = subject).first()
            if subject_exist is None:
                return JsonResponse({'messgae':'subject is not Instance'},status=400)
            exam_exist = ExamMapping.objects.filter(exam = exam_type).first()
            if exam_exist is None:
                return JsonResponse({'message':'exam type is not an Instance'},status=400)
            department_exist = Mapping.objects.filter(id = department).first()
            if department_exist is None:
                return JsonResponse({'message':'department is not an Instance'},status=400)
            if faculty_exist:
                paper,created=QuestionPaper.objects.get_or_create(
                                            exam_type=exam_exist,
                                            subject=subject_exist,
                                            title="KIET Group Of Institutions",
                                            
                                            department=department_exist,
                                            # date=date,
                                            # start_time=start_time,
                                            defaults={"added_by" : faculty_exist.user,"questions":questions}
                                            
                                            )
                if created:
                    return JsonResponse({'message':'Created succesfully'},status=201)
                else:
                    return JsonResponse({'message':f'Question peper already created for {{department_exists__department__name}}'},status=409)
                
            else:
                return JsonResponse({'message':'You are not a Teacher'},status=403)
        else:
            return JsonResponse({'message':'You are not Authenticated'},status=401)
        

    elif request.method=='PUT':
        if request.user.is_authenticated:
            id=Roles.objects.get(role_name='Teacher',deleted_status=False)
            faculty=UserRole.objects.filter(user=request.user.id,role_id = id.id).first()
            id=Roles.objects.get(role_name='Admin',deleted_status=False)
            admin=UserRole.objects.filter(user=request.user.id,role_id = id.id).first()
            
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
            id=Roles.objects.get(role_name='Teacher',deleted_status=False)
            faculty=UserRole.objects.filter(user=request.user.id,role_id = id.id).first()
            id=Roles.objects.get(role_name='Admin',deleted_status=False)
            admin=UserRole.objects.filter(user=request.user.id,role_id = id.id).first()

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
        
    elif request.method=='GET':
        subject_id=request.GET.get('id') 
        if subject_id is None or not subject_id:
            return JsonResponse({'message':'You are not sending subject id'},status=400)
        student=Student.objects.filter(user=request.user.id).first()
        if student is None:
            return JsonResponse({'message':''})
        print(student)
        data=QuestionPaper.objects.filter(department=student.department,subject=subject_id).values()
        return JsonResponse(list(data),safe=False)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)


def paper_response(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            id=Roles.objects.get(role_name='Student',deleted_status=False)
            student=UserRole.objects.filter(user=request.user.id,role_id = id.id).first()

            load = json.loads(request.body)

            answer=load.get('answer')
            paper_id = load.get('paper_id')

            if answer is None or paper_id is None :
                return JsonResponse({'message':'Missing value of any key'},status=400)
            if not answer or not paper_id :
                return JsonResponse({'message':'Missing Required Field'},status=400)
            
            paper_exist = QuestionPaper.objects.filter(id = paper_id).first()
            if paper_exist is None:
                return JsonResponse({'message':'paper is not an Instance'})
            
            if student:
                PaperResponse.objects.create(
                    answer=answer,
                    paper = paper_exist,
                    added_by = student.user,
                )    
                return JsonResponse({'message':'Created succesfully'},status=201)
            else:
                return JsonResponse({'message':'You are not a Teacher'},status=403)
        else:
            return JsonResponse({'message':'You are not Authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)
    

def paper_evaluation(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            id=Roles.objects.get(role_name='Teacher',deleted_status=False)
            faculty=UserRole.objects.filter(user=request.user.id,role_id = id.id).first()

            load=json.loads(request.body)

            paper_id=load.get('paper_id')
            evaluation=load.get('evaluation')

            if faculty:
                evaluated=PaperResponse.objects.filter(pk=paper_id,deleted_status=False).update(
                evaluation=evaluation,
                checked_status=True,
                checked_time=datetime.now(),
                checked_by=faculty.user
                )
                if evaluated:
                    return JsonResponse({'message':'Paper checked'})
                else:
                    return JsonResponse({'message':'No content'},status=204)
            else:
                return JsonResponse({'message':'You are not autherised'},status=403)
        else:
            return JsonResponse({'message':'You are not logged in'},status=401)
        
    elif request.method == 'PUT':
        if request.user.is_authenticated:
            id=Roles.objects.get(role_name='Teacher',deleted_status=False)
            faculty=UserRole.objects.filter(user=request.user.id,role_id = id.id).first()

            load=json.loads(request.body)

            paper_id=load.get('paper_id')
            evaluation=load.get('evaluation')

            if faculty:
                evaluated=PaperResponse.objects.filter(pk=paper_id,deleted_status=False).update(evaluation=evaluation,
                                                                                      checked_time=datetime.now(),
                                                                                      )
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
            id=Roles.objects.get(role_name='Teacher',deleted_status=False)
            faculty=UserRole.objects.filter(user=request.user.id,role_id = id.id).first()

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


def exam_type(request):
    if request.method == 'GET':
        data=Dropdown.objects.get(deleted_status=False,name='Exam Type')
        print(data)
        exam_type=Dropdown.objects.filter(deleted_status=False,relation=data).values('pk','name')
        if exam_type:
            return JsonResponse(list(exam_type),safe=False)
        else:
            return JsonResponse({'message':'No Content'},status=204)

    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)

def exam_info(request):
    if request.method == 'GET':
        id=request.GET.get('id')
        data=ExamMapping.objects.filter(deleted_status=False,exam=id).values('marks__name','duration__name')
        
        if data:
            return JsonResponse(list(data),safe=False)
        else:
            return JsonResponse({'message':'No Content'},status=204)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)

def exam_mapping(request):
    if request.method =='POST':
        if request.user.is_authenticated:
            id=Roles.objects.filter(role_name='Admin',deleted_status=False).first()
            if id:
                admin_exist=UserRole.objects.filter(user=request.user.id,role_id = id.pk,deleted_status=False).first()
                load = json.loads(request.body)
                exam_type = load.get('exam_type_id')
                duration=load.get('duration')
                marks = load.get('marks')
                print(admin_exist.user.id)
                if duration is None or marks is None or exam_type is None :
                    return JsonResponse({'message':'Missing value of any key'},status=400)
                if not duration or not marks or not exam_type :
                    return JsonResponse({'message':'Missing Required Field'},status=400)
                exam_exist = Dropdown.objects.filter(pk = exam_type).first()
                if exam_exist is None:
                    return JsonResponse({'message':'exam_type Not an Instance'},status=400)
                duration_exist = Dropdown.objects.filter(pk = duration).first()
                if duration_exist is None:
                    return JsonResponse({'messgae':'duration is not an Instance'})
                marks_exist = Dropdown.objects.filter(pk = marks).first()
                if marks_exist is None:
                    return JsonResponse({'message':'marks is not an Instance'})
                if admin_exist:
                    mapping, created = ExamMapping.objects.get_or_create(
                        duration=duration_exist,
                        exam=exam_exist,
                        marks=marks_exist,
                        added_by=admin_exist.user
                    )
                    if created:
                        # return JsonResponse({'message':f'{exam_exist.name} conduct for {marks_exist.name} marks for {duration_exist.name} minutes'})
                        return JsonResponse({'message':'Exam Mapping successfully done'})
                    else:
                        return JsonResponse({'message':'exam already exist'},status=409)
                else:
                    return JsonResponse({'message':'admin not found'},status=204)
        else:
            return JsonResponse({'message':'user is not authenticated'},status=403)
    else:
        return JsonResponse({'message':'invalid request method'},status=405)


def department_course(request):
    if request.method == 'GET':
        id=Faculty.objects.filter(user=request.user.id).first()
        # if not id :
        #     return JsonResponse()
        data=SubjectTeacherMapping.objects.filter(deleted_status=False,faculty=id).values('subject__department__pk','subject__department__department__name','subject__department__course__name').distinct()
        if data:
            return JsonResponse(list(data),safe=False)
        else:
            return JsonResponse({'message':'No Content'},status=204)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)
            
            
def subject_year(request):
    if request.method == 'GET':
        department_id=request.GET.get('dept_id')
        if department_id is None:
            return JsonResponse({'message':'You are not sending department_id'})
        data=SubjectMapping.objects.filter(deleted_status=False,department=department_id).values('subject__pk','year','subject__subject_name','subject__subject_code')
        if data:
            return JsonResponse(list(data),safe=False)
        else:
            return JsonResponse({'message':'No Content'},status=204)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)
            
            
def access_question(request):
    if request.method=='GET':
        student=Student.objects.filter(user=request.user.id).first()
        print(student.department)
        data=SubjectMapping.objects.filter(department=student.department).values('pk','subject__subject_name')
        return JsonResponse(list(data),safe=False)
    else:
        return JsonResponse({'message':'Invalid'},status=405)     

def get_question_paper(request):
    if request.method=='GET':
        subject_id=request.GET.get('id') 
        student=Student.objects.filter(user=request.user.id).first()
        data=QuestionPaper.objects.filter(department=student.department,subject=subject_id).values()
        return JsonResponse(list(data),safe=False)
    else:
        return JsonResponse({'message':'Invalid'},status=405)
    

def datesheet_maping(request):
    if request.user.is_authenticated:
        id=Roles.objects.get(role_name='Admin',deleted_status=False)
        admin=UserRole.objects.filter(user=request.user.id,role_id = id.pk,deleted_status=False).first()
        if admin:
            if request.method == 'POST':

                load=json.loads(request.body)
    
                subject=load.get('subject')
                exam_map=load.get('exam_map')
                shift=load.get('shift')
                date=load.get('date')
                start_time=load.get('start_time')

                if subject is None or exam_map is None or shift is None or date is None or start_time is None:
                    return JsonResponse({'message':'Missing any key'},status=400)
                if not subject or not exam_map or not shift or not date or not start_time:
                    return JsonResponse({'message':'Missing required field'},status=400)
                
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
                defaults={"added_by":admin.user}
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
                
                
