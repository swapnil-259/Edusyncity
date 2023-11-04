from django.urls import path
from EduAdmin import views

urlpatterns = [
    path('register_faculty/', views.register_faculty),
    path('register_student/', views.register_student),
    path('login/', views.login_user),
    path('change_password/',views.change_password),
    path('logout/', views.logout_user),
    path('add_role/', views.add_role),
    path('child/', views.child),
    path('left_panel/',views.left_panel),
    path('personal_info/',views.get_personal_info),
    # path('assign_department/',views.assign_department_to_course, name='assign_department_to_course'),
]
  