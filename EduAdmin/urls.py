from django.urls import path
from EduAdmin import views

urlpatterns = [
    path('register_faculty/', views.register_faculty, name='register_faculty'),
    path('register_student/', views.register_student, name = 'register_student'),
    path('login/', views.login_user, name = 'login'),
    path('change_password/',views.change_password, name = 'change_password'),
    path('logout/', views.logout_user),
    path('add_role/', views.add_role, name = 'add_role'),
    path('child/', views.child, name='child'),
    path('left_panel/',views.left_panel, name='left_panel')
    # path('subject/',views.subject, name = 'subject'),
    # path('assign_department/',views.assign_department_to_course, name='assign_department_to_course'),
]
  