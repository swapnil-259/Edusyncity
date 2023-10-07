from django.shortcuts import render
from .models import User, UserRole


def RegisterFaculty(request):
    if request.method == 'POST':
        