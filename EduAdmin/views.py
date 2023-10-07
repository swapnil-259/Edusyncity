from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import User, UserRole, Roles, Faculty
from django.http import JsonResponse
import json


def register_faculty(request):
    if request.method == 'POST':
      first_name = request.POST.get('firstname')
      last_name = request.POST.get('lastname')
      user_name =  request.POST.get('username')
      email =  request.POST.get('email')
      gender =  request.POST.get('gender')
      phone =  request.POST.get('phone')
      age =  request.POST.get('age')
      address =  request.POST.get('address')
      department =  request.POST.get('department')
      qualification = request.POST.get('qualification')
      subject =  request.POST.get('subject')
      profile_pic = request.FILES.get('profilepic')
      password =  request.POST.get('password')
      confirm_pass =  request.POST.get('confirmpassword')
      if password != confirm_pass:
            return JsonResponse({'message': 'Password and confirmPassword do not match'}, status=400)
      if user_name or first_name or last_name or email or gender or phone or age or address or password or confirm_pass== None:
            return JsonResponse({'message':'all details is mandatory'}, status = 400)
        
      user=  User.objects.create_user(
               username = user_name,
               password = password,
               first_name=first_name,
               last_name=last_name,
               email=email
             ) 
      Faculty.objects.create(
          user_id = user.id,
          department_id = department,
          subject_id = subject,
          qualification = qualification,
          address = address,
          profile_picture = profile_pic   
      )
      roles, created = Roles.objects.get_or_create(rolename= 'Faculty')
      UserRole.objects.create(
          user_id = user.id,
          role_id = roles.id,
          department = department
      )
        
        