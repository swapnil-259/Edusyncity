from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import PaperDetails,Questions
from EduAdmin.models import UserRole,Dropdown,Mapping,Subjects,User

def paper_details(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            # admin=UserRole.objects.filter(user=request.user.id,role_id = '1').first()
            faculty=UserRole.objects.filter(user=request.user.id,role_id = '2').first()
    
            load=json.loads(request.body)

            course=load.get('course')
            department=load.get('department')
            exam_type=load.get('exam_type')
            subject=load.get('subject')
            title=load.get('title')
            paper_code=load.get('paper_code')
            set=load.get('set')
            shift=load.get('shift')
            start_time=load.get('start_time')
            end_time=load.get('end_time')
            total_marks=load.get('total_marks')
            if course is None or department is None or exam_type is None or subject is None or title is None or paper_code is None or set is None or shift is None or start_time is None or end_time is None or total_marks is None:
                return JsonResponse({'message':'Missing value of any key'},status=400)
            if not course or not department or not exam_type or not subject or not title or not paper_code or not set or not shift or not start_time or not end_time or not total_marks:
                return JsonResponse({'message':'Missing Required Field'},status=400)
                
            if faculty:
                PaperDetails.objects.create(course=course,
                                            department=department,
                                            exam_type=exam_type,
                                            subject=subject,
                                            title=title,
                                            paper_code=paper_code,
                                            set=set,
                                            shift=shift,
                                            start_time=start_time,
                                            end_time=end_time,
                                            total_marks=total_marks
                                            )
                return JsonResponse({'message':'Created succesfully'},status=201)
            else:
                return JsonResponse({'message':'You are not Autherised'},status=403)
        else:
            return JsonResponse({'message':'You are not Authenticated'},status=401)
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=405)
    

# def ()