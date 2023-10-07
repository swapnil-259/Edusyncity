from django.urls import path
from EduAdmin import views

urlpatterns = [
      path('register_faculty/', views.register_faculty, name='register_faculty'),

]
  