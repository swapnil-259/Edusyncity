from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class BaseModel(models.Model):
    created_time=models.DateTimeField(auto_now_add=True)
    deleted_status = models.BooleanField(default=0)
    deleted_time = models.DateTimeField(null=True)
    added_by= models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    
    class Meta:
        abstract = True

class Dropdown(BaseModel):
    name = models.CharField(null = True, max_length=100)
    relation = models.ForeignKey("Dropdown", on_delete=models.SET_NULL, null=True)
    can_delete=models.BooleanField(default=False)
    can_update=models.BooleanField(default=False)
    child=models.PositiveIntegerField(default='0')
    order_by=models.PositiveIntegerField(default=0)
    icon=models.TextField(max_length=100,null=True)
    type=models.TextField(max_length=100,null=True)
    state=models.TextField(max_length=100,null=True)
    pannel=models.BooleanField(default=0)
    year = models.PositiveIntegerField(null=True)

class Mapping(BaseModel):
    course = models.ForeignKey(Dropdown, null=True, on_delete=models.SET_NULL, related_name='course_name')
    department = models.ForeignKey(Dropdown, null=True, on_delete=models.SET_NULL, related_name='department_name')
    
class Roles(BaseModel):
    role_name=models.CharField(max_length=50,null=True)

class UserRole(BaseModel):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='user_identity')
    # department=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True)
    role=models.ForeignKey(Roles,on_delete=models.SET_NULL,null=True)
    
class Subjects(BaseModel):
    course=models.ForeignKey(Dropdown,on_delete=models.SET_NULL, null=True,related_name='course_identity')
    department=models.ForeignKey(Dropdown,on_delete=models.SET_NULL, null=True)
    year = models.PositiveIntegerField(null=True)
    subject_name = models.CharField(max_length=100, null=True)
    subject_code = models.CharField(max_length=50, null=True)

class Faculty(BaseModel):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="faculty_identity")
    course = models.ForeignKey(Dropdown, on_delete=models.SET_NULL, null=True, related_name='faculty_course')
    department=models.ForeignKey(Dropdown,on_delete=models.SET_NULL, null=True)
    subject=models.ForeignKey(Subjects,on_delete=models.SET_NULL,null=True)
    age = models.PositiveIntegerField(null= True)
    gender = models.CharField(max_length=10, null= True)
    qualification=models.CharField(null=True,max_length=100)
    address = models.CharField(max_length=200, blank=True)
    contact = models.PositiveIntegerField(null=True)
   
class Student(BaseModel):
    user =models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="student_identity")
    course = models.ForeignKey(Dropdown, on_delete=models.SET_NULL, null=True, related_name='student_course')
    department=models.ForeignKey(Dropdown,on_delete=models.SET_NULL, null=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(null=True, max_length=100)
    address = models.CharField(max_length=200, blank=True)
    year = models.ForeignKey(Dropdown, on_delete=models.SET_NULL, null=True, related_name='student_year')
    contact = models.PositiveIntegerField(null=True)
    father_name = models.CharField(null=True, max_length=200)
    mother_name = models.CharField(max_length=200, null=True)

    
  

    
   