from django.urls import path
from EduAdmin import views

urlpatterns = [
      path('register_faculty/', views.register_faculty, name='register_faculty'),
     path('login/', views.login_user, name = 'login'),
     path('logout/', views.logout_user),
     path('add_role/', views.add_role, name = 'add_role'),
     path('add_course/', views.add_course, name = 'add_course'),

]
  