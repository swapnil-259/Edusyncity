from django.urls import path
from EduCore import views

urlpatterns = [
    path('sidebar/',views.sidebar, name='sidebar'),
    path('courses/',views.courses, name='courses'),
    path('departments/',views.departments, name='departments'),
    path('years/',views.years, name='years'),
    path('subject/',views.subject, name = 'subject')
]