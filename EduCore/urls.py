from django.urls import path
from EduCore import views

urlpatterns = [
    path('sidebar/',views.sidebar),
    path('loggedin/',views.logged_in),
    path('get_parents/',views.get_parents),
    path('get_childs/',views.get_childs),
    path('departments/',views.departments),
    path('subjects/',views.subjects),
    path('years/',views.years),
    path('subject/', views.subject),
    path('get_subjects/',views.get_subjects),
    path('parents/',views.parents),
    path('subject_teacher_mapping/',views.subject_teacher_mapping),
    path('subject_mapping/',views.subject_mapping),
    path('<dropdown>',views.dropdown_option),
    path('assign_department_to_course/',views.assign_department_to_course),
    path('get_departments/',views.get_departments),
    path('get_years/',views.get_years),
    path('faculty/',views.faculty),
    path('mapped_faculty/',views.mapped_faculty),
    # path('get_courses/',views.get_courses, name='get_courses'),
    path('admin_chart/',views.admin_chart),
]