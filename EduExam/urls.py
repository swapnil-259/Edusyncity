from django.urls import path
from EduExam import views

urlpatterns = [
    path('examtype/',views.exam_type, name='examtype'),
    path('examinfo/',views.exam_info, name='examinfo'),
  path('question_paper/',views.question_paper, name ='question_paper'),
  path('paper_response/',views.paper_response, name ='paper_response'),
  path('exam_mapping/',views.exam_mapping, name='exam_mapping'),
  path('department_course/',views.department_course, name='department_course'),
  path('subject_year/',views.subject_year, name='subject_year'),
  path('accesquestion/',views.access_question, name='acces_question'),

  
    
]