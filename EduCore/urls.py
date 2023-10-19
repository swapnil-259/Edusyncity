from django.urls import path
from EduCore import views

urlpatterns = [
    path('sidebar/',views.sidebar, name='sidebar'),
    path('loggedin/',views.logged_in, name='loggedin'),
    path('parents/',views.parents, name='parents'),
    path('childs/',views.childs, name='childs'),
    path('courses/',views.courses, name='courses'),
    path('departments/',views.departments, name='departments'),
    path('years/',views.years, name='years'),
    path('subjects/', views.subjects,name='subjects'),
    path('gender/', views.gender, name='gender'),
    path('title/', views.title, name='title'),
    path('religion/', views.religion, name='religion'),
]