from django.db import models
from EduAdmin.models import User
from EduAdmin.models import Dropdown,Subjects

class BaseModel(models.Model):
    created_time=models.DateTimeField(auto_now_add=True)
    deleted_status = models.BooleanField(default=0)
    deleted_time = models.DateTimeField(null=True)
    edited_date=models.DateTimeField(null=True)
    added_by= models.ForeignKey(User,on_delete=models.SET_NULL, null=True,related_name='added_iden')
    # edited_by= models.ForeignKey(User,on_delete=models.SET_NULL, null=True,related_name='edited_ident')
    
    class Meta:
        abstract = True

class PaperDetails(BaseModel):
    course=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='course_identity')
    department=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='department_identity')
    exam_type=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='exam_type')
    subject=models.ForeignKey(Subjects,on_delete=models.SET_NULL,null=True)
    title=models.TextField(max_length=100,null=True)
    paper_id=models.CharField(max_length=30,null=True)
    set=models.CharField(max_length=10,null=True)
    shift=models.CharField(max_length=20,null=True)
    strart_time=models.DateTimeField(null=True)
    end_time=models.DateTimeField(null=True)
    checked_satus=models.BooleanField(default=False)
    checked_time=models.DateTimeField(null=True)
    score=models.IntegerField(null=True)
    checked_by=models.ForeignKey(User,on_delete=models.SET_NULL, null=True,related_name='checked_by')
    
class Questions(BaseModel):
    paper=models.ForeignKey(PaperDetails,on_delete=models.SET_NULL,null=True)
    question_id=models.IntegerField(null=True)
    question=models.TextField(max_length=1000,null=True)
    max_marks=models.PositiveIntegerField(null=True)
    answer=models.TextField(max_length=1000,blank=True)

class QuestionOptions(BaseModel):
    question=models.ForeignKey(Questions,on_delete=models.SET_NULL,null=True)
    option=models.TextField(max_length=200,null=True)
