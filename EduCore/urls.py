from django.urls import path
from EduCore import views

urlpatterns = [
    path('sidebar/',views.sidebar, name='sidebar'),
    path('parents/',views.parents, name='parents'),
    path('childs/',views.childs, name='childs'),
    path('courses/',views.courses, name='courses'),
    path('departments/',views.departments, name='departments'),
    path('years/',views.years, name='years'),
    path('subject/',views.subject, name = 'subject'),
    path('subjects/', views.subjects,name='subjects')
]