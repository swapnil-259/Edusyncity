from django.db import models
from EduAdmin.models import Dropdown,BaseModel,Faculty,Mapping

class Subject(BaseModel):
    subject_name = models.CharField(max_length=100, null=True)
    subject_code = models.CharField(max_length=50, null=True)
    

class SubjectMapping(BaseModel):
    subject = models.ForeignKey(Subject,on_delete=models.SET_NULL,null=True,related_name='identify_subject')
    department=models.ForeignKey(Mapping,on_delete=models.SET_NULL, null=True)
    year=models.PositiveIntegerField(null=True)

class SubjectTeacherMapping(BaseModel):
    subject = models.ForeignKey(SubjectMapping,on_delete=models.SET_NULL,null=True,related_name='identify_mapped_subjects')
    faculty = models.ForeignKey(Faculty,on_delete=models.SET_NULL,null=True)
    