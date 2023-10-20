from django.urls import path
from EduExam import views

urlpatterns = [
    path('examtype/',views.exam_type, name='examtype'),
    path('examinfo/',views.exam_info, name='examinfo'),
]