from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Basemodel(models.Model):
    created_time=models.DateTimeField(auto_now=True)
    deleted_status=models.BooleanField(default=False)
    deleted_time=models.DateTimeField(null=True)


class DepartmentUnderCourses(Basemodel):
    name = models.CharField(null = True, max_length=100)
    course = models.ForeignKey("DepartmentUnderCourses", on_delete=models.CASCADE)
    


class Roles(Basemodel):
    role_name=models.CharField(max_length=50,null=True)

class UserRole(Basemodel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    department=models.ForeignKey(DepartmentUnderCourses,on_delete=models.CASCADE,null=True)
    role=models.ForeignKey(Roles,on_delete=models.CASCADE,null=True)
   


class Faculty(Basemodel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    department=models.ForeignKey(DepartmentUnderCourses,on_delete=models)
    subject=models.ForeignKey(Subjects,on_delete=models.CASCADE,null=True)
    qualification=models.CharField(null=True,max_length=100)