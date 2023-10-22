from django.urls import path
from EduCore import views

urlpatterns = [
    path('sidebar/',views.sidebar, name='sidebar'),
    path('loggedin/',views.logged_in, name='loggedin'),
    path('get_parents/',views.get_parents, name='get_parents'),
    path('get_childs/',views.get_childs, name='get_childs'),
    path('departments/',views.departments, name='departments'),
    path('subjects/',views.subjects),
    path('years/',views.years, name='years'),
    path('subject/', views.subject,name='subject'),
    
    path('parents/',views.parents,name='parents'),
    path('subject_teacher_mapping/',views.subject_teacher_mapping, name='subject_teacher_mapping'),
    path('<dropdown>',views.dropdown_option,name='dropdown'),
    path('assign_department_to_course/',views.assign_department_to_course,name='assign_department_to_course'),
    path('get_departments/',views.get_departments, name='get_departments'),
    path('get_years/',views.get_years, name='get_years')
    # path('get_courses/',views.get_courses, name='get_courses')
]