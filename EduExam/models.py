from django.db import models
from EduAdmin.models import BaseModel
from EduAdmin.models import Dropdown,Subjects,User
from jsonfield import JSONField


class ExamMapping(BaseModel):
    exam=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='exam_identity')
    marks=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='marks_identity')
    duration=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='duration_identity')


class PaperDetails(BaseModel):
    course=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='course_idty')
    department=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='department_identity')
    exam_type=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='exam_type')
    subject=models.ForeignKey(Subjects,on_delete=models.SET_NULL,null=True)
    title=models.TextField(max_length=100,null=True)
    paper_code=models.CharField(max_length=30,null=True)
    set=models.CharField(max_length=10,null=True)
    shift=models.CharField(max_length=20,null=True)
    date=models.DateField(null=True)
    strart_time=models.TimeField(null=True)
    end_time=models.TimeField(null=True)
    total_marks=models.IntegerField(null=True)
    
    
class Questions(BaseModel):
    paper=models.ForeignKey(PaperDetails,on_delete=models.SET_NULL,null=True)
    question=JSONField(max_length=1000,null=True)
    answer=JSONField(max_length=1000,blank=True)
    obtained_marks=models.PositiveIntegerField(null=True)
    checked_satus=models.BooleanField(default=False)
    checked_time=models.DateTimeField(null=True)
    checked_by=models.ForeignKey(User,on_delete=models.SET_NULL, null=True,related_name='checked_by')

# class QuestionOptions(BaseModel):
#     question=models.ForeignKey(Questions,on_delete=models.SET_NULL,null=True)
#     option=models.TextField(max_length=200,null=True)
