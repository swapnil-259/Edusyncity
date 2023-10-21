from django.urls import path
from EduCore import views

urlpatterns = [
    path('sidebar/',views.sidebar, name='sidebar'),
    path('loggedin/',views.logged_in, name='loggedin'),
    path('get_parents/',views.get_parents, name='get_parents'),
    path('get_childs/',views.get_childs, name='get_childs'),
    path('courses/',views.courses, name='courses'),
    path('departments/',views.departments, name='departments'),
    path('years/',views.years, name='years'),
    # path('subjects/', views.subjects,name='subjects'),
    path('gender/', views.gender, name='gender'),
    path('title/', views.title, name='title'),
    path('religion/', views.religion, name='religion'),
    path('parents/',views.parents,name='parents')
]