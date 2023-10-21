from django.urls import path
from EduExam import views

urlpatterns = [
    path('examtype/',views.exam_type, name='examtype'),
    path('examinfo/',views.exam_info, name='examinfo'),
  path('paper_details/',views.paper_details, name ='paper_details'),
  path('exam_mapping/',views.exam_mapping, name='exam_mapping')
    
]