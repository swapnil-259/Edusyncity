from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import json
import re
from .models import User,Roles, UserRole, Faculty
from django.contrib.auth import authenticate,login,logout


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

def login_user(request):
    
    if request.method == 'POST':

        load=json.loads(request.body)
        username = load.get('username')
        password = load.get('password')
        user=authenticate(username=username,password=password)
        
        if username is None or password is None:
            return JsonResponse({'message': 'Missing any Key.'}, status=400)
        
        if not username or not password:
            return JsonResponse({'message': 'Missing Required field.'}, status=400)
        
        if user is not None:
            login(request,user)
            user_exist = UserRole.objects.filter(user_id = request.user.id).values('role','role__rolename')
            user_data = list(user_exist)
            return JsonResponse(user_data, safe=False)
        else:
            return JsonResponse({'message':'Incorrect Username Or password'},status=401)
        
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=400)

def logout_user(request):      
    if request.method == 'GET':
        
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'message':'Logged Out Succesfully'},status=200)
        else:
            return JsonResponse({'message':'User Is Not Authenticated'},status=401) 
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=400)    


        
        