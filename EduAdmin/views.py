from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import json
import re
from .models import User,Roles
from django.contrib.auth import authenticate,login,logout

def login_user(request):
    
    if request.method == 'POST':

        load=json.loads(request.body)
        email = load.get('email')
        password = load.get('password')
        user=authenticate(email=email,password=password)
        
        if email is None or password is None:
            return JsonResponse({'message': 'Missing any Key.'}, status=400)
        
        if not email or not password:
            return JsonResponse({'message': 'Missing Required field.'}, status=400)
        
        if user is not None:
            login(request,user)

            role =Roles.objects.get(user=request.user.id)
            if not role:
                return JsonResponse({'message':'Yo Not Have Any role'})
            else:
                return JsonResponse({'message':'You Are logged in','role':role.name})
            
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
