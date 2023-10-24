from django.db import models
from EduAdmin.models import BaseModel,Dropdown,Faculty,User
from jsonfield import JSONField
from EduCore.models import SubjectMapping,Subject
from EduAdmin.models import Mapping



class ExamMapping(BaseModel):
    exam=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='exam_identity')
    marks=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='marks_identity')
    duration=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='duration_identity')

class DateSheetMapping(BaseModel):
    exam_mapping=models.ForeignKey(ExamMapping,on_delete=models.SET_NULL,null=True,related_name='exammap_identity')
    course_department=models.ForeignKey(Mapping,on_delete=models.SET_NULL,null=True,related_name='course_dept_idty')
    year=models.PositiveIntegerField(null=True)
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)
    # shift=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='shift_identity')
    
class DateSheet(BaseModel):
    subject=models.ForeignKey(Subject,on_delete=models.SET_NULL,null=True)
    datesheet_mapping=models.ForeignKey(DateSheetMapping,on_delete=models.SET_NULL,null=True)
    shift=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='shift_identity')
    date=models.DateField(null=True)
    start_time=models.TimeField(null=True)

   

    

class QuestionPaper(BaseModel):
    exam_type=models.ForeignKey(ExamMapping,on_delete=models.SET_NULL,null=True,related_name='exam_type')
    date_sheet=models.ForeignKey(DateSheet,on_delete=models.SET_NULL,null=True)
    department=models.ForeignKey(Mapping,null=True,on_delete=models.SET_NULL,related_name='department_identity')
    subject=models.ForeignKey(SubjectMapping,on_delete=models.SET_NULL,null=True)
    set=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='set_identity')
    questions=JSONField(max_length=1000,null=True)
    
    
    
class PaperResponse(BaseModel):
    paper=models.ForeignKey(QuestionPaper,on_delete=models.SET_NULL,null=True)
    answer=JSONField(max_length=1000,blank=True)
    evaluation=JSONField(max_length=1000,blank=True)
    checked_satus=models.BooleanField(default=False)
    checked_time=models.DateTimeField(null=True)
    checked_by=models.ForeignKey(Faculty,on_delete=models.SET_NULL, null=True,related_name='checked_by')


    