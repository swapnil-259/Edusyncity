from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import PaperDetails,Questions
from EduAdmin.models import UserRole,Dropdown,Mapping,Subjects,User

def paper_details(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            faculty=UserRole.objects.filter(user=request.user.id,role_id = '2').first()
            load=json.loads(request.body)
            course=load.get('course')
            department=load.get('department')
            exam_type=load.get('exam_type')
            subject=load.get('subject')
            # title=load.get('title')
            paper_code=load.get('paper_code')
            # set=load.get('set')
            shift=load.get('shift')
            # start_time=load.get('start_time')
            # end_time=load.get('end_time')
            total_marks=load.get('total_marks')
            if course is None or department is None or exam_type is None or subject is None or paper_code is None or set is None or shift is None or total_marks is None:
                return JsonResponse({'message':'Missing value of any key'},status=400)
            if not course or not department or not exam_type or not subject  or not paper_code or not set or not shift or  not total_marks:
                return JsonResponse({'message':'Missing Required Field'},status=400)
            department_exist = Mapping.objects.filter(department = department).first()
            if department_exist is None:
                return JsonResponse({'message':'Department Not an Instance'},status=400)
            course_exist = Dropdown.objects.filter(id = course).first()
            if course_exist is None:
                return JsonResponse({'message':'Course Not an Instance'},status=400)
            subject_exist = Subjects.objects.filter(id = subject).first()
            if subject_exist is None:
                return JsonResponse({'messgae':'subject is not Instance'})
            exam_exist = Dropdown.objects.filter(id = exam_type).first()
            if exam_exist is None:
                return JsonResponse({'message':'exam type is not an Instance'})
            # set_exist = Dropdown.objects.filter(id = set).first()
            # if set_exist is None:
            #     return JsonResponse({'message':'exam type is not an Instance'})
            shift_exist = Dropdown.objects.filter(id = shift).first()
            if shift_exist is None:
                return JsonResponse({'message':'exam type is not an Instance'})
            marks = Dropdown.objects.filter(relation = exam_type).first()
            if marks is None:
                return JsonResponse({'message':'exam type is not an Instance'})
            if faculty:
                PaperDetails.objects.create(course=course_exist,
                                            department=department_exist.department,
                                            exam_type=exam_exist,
                                            subject=subject_exist,
                                            title="KIET Group Of Institutions",
                                            paper_code=paper_code,
                                            # set=set_exist.pk,
                                            shift=shift_exist.pk,
                                            # start_time=start_time,
                                            # end_time=end_time,
                                            total_marks=marks.name,
                                            added_by = faculty.user
                                            )
                
                return JsonResponse({'message':'Created succesfully'},status=201)
            else:
                return JsonResponse({'message':'You are not a Teacher'},status=403)
        else:
            return JsonResponse({'message':'You are not Authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)
def question_details(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            faculty = UserRole.objects.filter(role = '2', user = request.session.id).first()
            load = json.loads(request.body)
            question=load.get('question')
            paper_id = load.get('paper_id')
            if question is None or paper_id is None :
                return JsonResponse({'message':'Missing value of any key'},status=400)
            if not question or not paper_id :
                return JsonResponse({'message':'Missing Required Field'},status=400)
            paper_exist = PaperDetails.objects.filter(id = paper_id).first()
            if paper_exist is None:
                return JsonResponse({'message':'paper is not an Instance'})
            if faculty:
                Questions.objects.create(
                    question=question,
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
        # shift=Dropdown.objects.filter(deleted_status=False,relation='73')
        exam_type=Dropdown.objects.filter(deleted_status=False,relation='64').values('pk','name')
        if exam_type:
            return JsonResponse(list(exam_type),safe=False)
        else:
            return JsonResponse({'message':'No Content'},status=204)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)

def exam_info(request):
    if request.method == 'GET':
        id=request.GET.get('id')
        time=Dropdown.objects.filter(deleted_status=False,relation='80').values('name')
        marks=Dropdown.objects.filter(deleted_status=False,relation=id).values('name')
        data=[list(time),list(marks)]
        if time and marks:
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({'message':'No Content'},status=204)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)
