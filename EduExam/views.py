from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import QuestionPaper,PaperResponse,ExamMapping
from EduAdmin.models import UserRole,Dropdown,Mapping,Subjects,User,Roles



def question_paper(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            id=Roles.objects.get(role_name='Teacher',deleted_status=False)
            faculty=UserRole.objects.filter(user=request.user.id,role_id = id.id).first()
            
            load=json.loads(request.body)
            
            date=load.get('date')
            question=load.get('questions')
            exam_type=load.get('exam_type')
            subject=load.get('subject')
            # title=load.get('title')
            paper_code=load.get('paper_code')
            # set=load.get('set')
            # shift=load.get('shift')
            start_time=load.get('start_time')
            # end_time=load.get('end_time')
            # total_marks=load.get('total_marks')
            if date is None or question is None or exam_type is None or subject is None or paper_code is None or start_time is None:
                return JsonResponse({'message':'Missing value of any key'},status=400)
            if not date or not question or not exam_type or not subject  or not paper_code or not start_time:
                return JsonResponse({'message':'Missing Required Field'},status=400)
            # department_exist = Mapping.objects.filter(department = department).first()
            # if department_exist is None:
            #     return JsonResponse({'message':'Department Not an Instance'},status=400)
            # course_exist = Dropdown.objects.filter(id = course).first()
            # if course_exist is None:
            #     return JsonResponse({'message':'Course Not an Instance'},status=400)
            subject_exist = Subjects.objects.filter(id = subject).first()
            if subject_exist is None:
                return JsonResponse({'messgae':'subject is not Instance'})
            exam_exist = Dropdown.objects.filter(id = exam_type).first()
            if exam_exist is None:
                return JsonResponse({'message':'exam type is not an Instance'})
            # set_exist = Dropdown.objects.filter(id = set).first()
            # if set_exist is None:
            #     return JsonResponse({'message':'exam type is not an Instance'})
            # shift_exist = Dropdown.objects.filter(id = shift).first()
            # if shift_exist is None:
            #     return JsonResponse({'message':'exam type is not an Instance'})
            # marks = Dropdown.objects.filter(relation = exam_type).first()
            # if marks is None:
            #     return JsonResponse({'message':'exam type is not an Instance'})
            if faculty:
                QuestionPaper.objects.create(
                                            exam_type=exam_exist,
                                            subject=subject_exist,
                                            title="KIET Group Of Institutions",
                                            paper_code=paper_code,
                                            questions=question,
                                            # set=set_exist.pk,
                                            # shift=shift_exist.pk,
                                            date=date,
                                            start_time=start_time,
                                            added_by = faculty.user
                                            )
                
                return JsonResponse({'message':'Created succesfully'},status=201)
            else:
                return JsonResponse({'message':'You are not a Teacher'},status=403)
        else:
            return JsonResponse({'message':'You are not Authenticated'},status=401)
        

    if request.method=='PUT':
        if request.user.is_authenticated:
            id=Roles.objects.get(role_name='Teacher',deleted_status=False)
            faculty=UserRole.objects.filter(user=request.user.id,role_id = id.id).first()
            id=Roles.objects.get(role_name='Admin',deleted_status=False)
            admin=UserRole.objects.filter(user=request.user.id,role_id = id.id).first()
            
            load=json.loads(request.body)
            
            date=load.get('date')
            question=load.get('questions')
            paper_code=load.get('paper_code')
            start_time=load.get('start_time')
            if date is None or question is None or paper_code is None or start_time is None:
                return JsonResponse({'message':'Missing value of any key'},status=400)
            if not date or not question or not paper_code or not start_time:
                return JsonResponse({'message':'Missing Required Field'},status=400)
           
            if faculty or admin:
                QuestionPaper.objects.filter().update(
                                            paper_code=paper_code,
                                            questions=question,
                                            date=date,
                                            start_time=start_time,
                                            )
                
                return JsonResponse({'message':'Created succesfully'},status=201)
            else:
                return JsonResponse({'message':'You are not a Teacher'},status=403)
        else:
            return JsonResponse({'message':'You are not Authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)

def paper_response(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            id=Roles.objects.get(role_name='Teacher',deleted_status=False)
            faculty=UserRole.objects.filter(user=request.user.id,role_id = id.id).first()

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
            
            if faculty:
                PaperResponse.objects.create(
                    answer=answer,
                    paper = paper_exist,
                    added_by = faculty.user,
                )    
                return JsonResponse({'message':'Created succesfully'},status=201)
            else:
                return JsonResponse({'message':'You are not a Teacher'},status=403)
        else:
            return JsonResponse({'message':'You are not Authenticated'},status=401)
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
            id=Roles.objects.get(role_name='Teacher',deleted_status=False)
            faculty=UserRole.objects.filter(user=request.user.id,role_id = id.pk,deleted_status=False).first()
            load = json.loads(request.body)
            exam_type = load.get('exam_type')
            duration=load.get('duration')
            marks = load.get('marks')
            if duration is None or marks is None :
                return JsonResponse({'message':'Missing value of any key'},status=400)
            if not duration or not marks or not exam_type :
                return JsonResponse({'message':'Missing Required Field'},status=400)
            exam_exist = Dropdown.objects.filter(id = exam_type).first()
            if exam_exist is None:
                return JsonResponse({'message':'Course Not an Instance'},status=400)
            duration_exist = Dropdown.objects.filter(id = duration).first()
            if duration_exist is None:
                return JsonResponse({'messgae':'subject is not Instance'})
            marks_exist = Dropdown.objects.filter(id = marks).first()
            if marks_exist is None:
                return JsonResponse({'message':'exam type is not an Instance'})
            if faculty:
                mapping, created = ExamMapping.objects.get_or_create(
                    duration=duration_exist,
                    exam=exam_exist,
                    marks=marks_exist
                )
                if created:
                    return JsonResponse({'message':'exam is created'})
                else:
                    return JsonResponse({'message':'exam already exist'})
            else:
                return JsonResponse({'message':'admin not found'})
        else:
            return JsonResponse({'message':'user is not authenticated'})
    else:
        return JsonResponse({'message':'invalid request method'})
            
            
            
            
            
            
