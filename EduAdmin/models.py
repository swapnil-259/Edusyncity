from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class BaseModel(models.Model):
    created_time=models.DateTimeField(auto_now_add=True)
    deleted_status = models.BooleanField(default=0)
    deleted_time = models.DateTimeField(null=True)

class DepartmentUnderCourses(models.Model):
    courses_name = models.CharField(null = True, max_length=100)
    course = models.ForeignKey("Courses", on_delete=models.CASCADE)
    


class Roles(BaseModel):
    role_name=models.CharField(max_length=50,null=True)

class UserRole(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    department=models.ForeignKey(DepartmentUnderCourses,on_delete=models.CASCADE,null=True)
    role=models.ForeignKey(Roles,on_delete=models.CASCADE,null=True)
   


class Faculty(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    department=models.ForeignKey(DepartmentUnderCourses,on_delete=models)
    subject=models.ForeignKey(Subjects,on_delete=models.CASCADE,null=True)
    qualification=models.CharField(null=True,max_length=100)