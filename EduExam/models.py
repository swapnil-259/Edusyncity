from django.db import models
from EduAdmin.models import BaseModel,Dropdown,Faculty,User
from jsonfield import JSONField
from EduCore.models import SubjectMapping
from EduAdmin.models import Mapping


class ExamMapping(BaseModel):
    exam=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='exam_identity')
    marks=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='marks_identity')
    duration=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='duration_identity')
    
    
class QuestionPaper(BaseModel):
    exam_type=models.ForeignKey(ExamMapping,on_delete=models.SET_NULL,null=True,related_name='exam_type')
    department=models.ForeignKey(Mapping,null=True,on_delete=models.SET_NULL,related_name='department_identity')
    subject=models.ForeignKey(SubjectMapping,on_delete=models.SET_NULL,null=True)
    title=models.TextField(max_length=100,null=True)
    paper_code=models.CharField(max_length=30,null=True)
    set=models.CharField(max_length=10,null=True)
    shift=models.CharField(max_length=20,null=True)
    date=models.DateField(null=True)
    start_time=models.TimeField(null=True)
    questions=JSONField(max_length=1000,null=True)
    
    
    
class PaperResponse(BaseModel):
    paper=models.ForeignKey(QuestionPaper,on_delete=models.SET_NULL,null=True)
    answer=JSONField(max_length=1000,blank=True)
    evaluation=JSONField(max_length=1000,blank=True)
    checked_satus=models.BooleanField(default=False)
    checked_time=models.DateTimeField(null=True)
    checked_by=models.ForeignKey(Faculty,on_delete=models.SET_NULL, null=True,related_name='checked_by')


    