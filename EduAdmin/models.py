from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Courses(models.Model):
    courses_name = models.CharField(null = True, max_length=100)
    course = models.ForeignKey("Courses", on_delete=models.CASCADE)

    
    
    
    