from django.db import models
from EduAdmin.models import User
from EduAdmin.models import BaseModel,Dropdown,Subjects

class BaseModel(models.Model):
    created_time=models.DateTimeField(auto_now_add=True)
    deleted_status = models.BooleanField(default=0)
    deleted_time = models.DateTimeField(null=True)
    edited_date=models.DateTimeField(null=True)
    added_by= models.ForeignKey(User,on_delete=models.SET_NULL, null=True,related_name='added_by')
    edited_by= models.ForeignKey(User,on_delete=models.SET_NULL, null=True,related_name='edited_by')
    
    class Meta:
        abstract = True

class PaperDetails(BaseModel):
    course=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='course_identity')
    department=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='department_identity')
    exam_type=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='exam_type')
    subject=models.ForeignKey(Subjects,on_delete=models.SET_NULL,null=True)
    paper_id=models.CharField(max_length=30,null=True)
    set=models.CharField(max_length=10,null=True)
    shift=models.CharField(max_length=20,null=True)
    strart_time=models.DateTimeField(null=True)
    end_time=models.DateTimeField(null=True)
    checked_satus=models.BooleanField(default=False)
    checked_time=models.DateTimeField(null=True)
    score=models.IntegerField(null=True)
    checked_by=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    
class Questions(BaseModel):
    paper=models.ForeignKey(PaperDetails,on_delete=models.SET_NULL,null=True)
    question_no=models.IntegerField(max_length=1000,null=True)
    question=models.TextField(max_length=1000,null=True)
    # option_1=models.CharField(max_length=)



   
