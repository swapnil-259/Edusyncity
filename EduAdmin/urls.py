from django.urls import path
from EduAdmin import views

urlpatterns = [
    path('register_faculty/', views.register_faculty, name='register_faculty'),
    path('register_student/', views.register_student, name = 'register_student'),
    path('login/', views.login_user, name = 'login'),
    path('forgot_password/',views.forgot_password, name = 'forgot_password'),
    path('logout/', views.logout_user),
    path('add_role/', views.add_role, name = 'add_role'),
    path('dropdown/', views.dropdown, name='dropdown'),
    path('subject/',views.subject, name = 'subject'),
    
    path('add_course/', views.add_course, name = 'add_course'),
    path('add_departments/', views.add_departments, name = 'add_departments'),
    path('assign_department/',views.assign_department_to_course, name='assign_department_to_course'),


]
  