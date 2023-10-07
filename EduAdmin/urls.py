from django.urls import path
from EduAdmin import views

urlpatterns = [
     path('login/', views.login_user),
     path('logout/', views.logout_user),

]
  