from django.urls import path
from EduExam import views

urlpatterns = [
  path('paper_details/',views.paper_details, name ='paper_details')
    
]