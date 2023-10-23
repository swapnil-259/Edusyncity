from django.urls import path
from EduExam import views

urlpatterns = [
    path('examtype/',views.exam_type),
    path('examinfo/',views.exam_info),
    path('question_paper/',views.question_paper),
    path('paper_response/',views.paper_response),
    path('exam_mapping/',views.exam_mapping),
    path('department_course/',views.department_course),
    path('subject_year/',views.subject_year),
    path('access_question/',views.access_question),
    path('get_question_paper/',views.get_question_paper),
    path('datesheet_mapping/',views.datesheet_maping)

  
    
]