from django.db import models
from django.contrib.auth.models import AbstractUser
# from EduExam.models import SubjectMapping

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
    role= models.PositiveIntegerField(null=True)

class Mapping(BaseModel):
    course = models.ForeignKey(Dropdown, null=True, on_delete=models.SET_NULL, related_name='course_name')
    department = models.ForeignKey(Dropdown, null=True, on_delete=models.SET_NULL, related_name='department_name')
    

class Roles(BaseModel):
    role_name=models.CharField(max_length=50,null=True)

class UserRole(BaseModel):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='user_identity')
    role=models.ForeignKey(Roles,on_delete=models.SET_NULL,null=True)
    

class Faculty(BaseModel):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="faculty_identity")
    age = models.PositiveIntegerField(null= True)
    gender = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='faculty_gender')
    qualification=models.CharField(null=True,max_length=100)
    address = models.CharField(max_length=200, blank=True)
    contact = models.BigIntegerField(null=True)
    title = models.ForeignKey(Dropdown, on_delete=models.SET_NULL, null=True, related_name='identify_title')
   
class Student(BaseModel):
    user =models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="student_identity")
    course = models.ForeignKey(Dropdown, on_delete=models.SET_NULL, null=True, related_name='student_course')
    department=models.ForeignKey(Mapping,on_delete=models.SET_NULL, null=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='student_gender')
    address = models.CharField(max_length=200, blank=True)
    year = models.PositiveIntegerField(null=True)
    contact = models.BigIntegerField(null=True)
    father_name = models.CharField(null=True, max_length=200)
    mother_name = models.CharField(max_length=200, null=True)
    religion = models.ForeignKey(Dropdown, on_delete=models.SET_NULL, null=True,related_name="student_religion")
    
class LeftPanel(BaseModel):
    name = models.CharField(null = True, max_length=100)
    relation = models.ForeignKey("LeftPanel", on_delete=models.SET_NULL, null=True)
    order_by=models.PositiveIntegerField(default=0)
    icon=models.TextField(max_length=100,null=True)
    type=models.TextField(max_length=100,null=True)
    state=models.TextField(max_length=100,null=True)
    panel=models.BooleanField(default=0)
    role= models.PositiveIntegerField(null=True)
    
    
  

    
   