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
    course=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='exam_course')
    year=models.PositiveIntegerField(null=True)
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)
    published=models.BooleanField(null=True,default=False)
    published_time=models.TimeField(null=True)
    
class DateSheet(BaseModel):
    subject=models.ForeignKey(Subject,on_delete=models.SET_NULL,null=True)
    datesheet_mapping=models.ForeignKey(DateSheetMapping,on_delete=models.SET_NULL,null=True)
    course_department=models.ForeignKey(Mapping,on_delete=models.SET_NULL,null=True,related_name='course_dept_idty')
    shift=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='shift_identity')
    date=models.DateField(null=True)
    start_time=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='start_time_identity')

class QuestionPaper(BaseModel):
    date_sheet=models.ForeignKey(DateSheet,on_delete=models.SET_NULL,null=True)
    subject=models.ForeignKey(SubjectMapping,on_delete=models.SET_NULL,null=True)
    exam_type=models.ForeignKey(ExamMapping,on_delete=models.SET_NULL,null=True,related_name='exam_type')
    department=models.ForeignKey(Mapping,null=True,on_delete=models.SET_NULL,related_name='department_identity')
    set=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='set_identity')
    # start_time=models.TimeField(null=True)
    questions=JSONField(max_length=1000,null=True)
    
    
class PaperResponse(BaseModel):
    paper=models.ForeignKey(QuestionPaper,on_delete=models.SET_NULL,null=True)
    answer=JSONField(max_length=1000,blank=True)
    evaluation=JSONField(max_length=1000,blank=True)
    total_marks=models.PositiveIntegerField(null=True)
    checked_status=models.BooleanField(default=False)
    checked_time=models.DateTimeField(null=True)
    checked_by=models.ForeignKey(User,on_delete=models.SET_NULL, null=True,related_name='checked_by')


    