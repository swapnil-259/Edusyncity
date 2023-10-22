from django.db import models
from EduAdmin.models import Dropdown,BaseModel,Faculty,Mapping

class Subject(BaseModel):
    subject_name = models.CharField(max_length=100, null=True)
    subject_code = models.CharField(max_length=50, null=True)
    

class SubjectMapping(BaseModel):
    subject = models.ForeignKey(Subject,on_delete=models.SET_NULL,null=True,related_name='identify_subject')
    department=models.ForeignKey(Mapping,on_delete=models.SET_NULL, null=True)
    year=models.PositiveIntegerField(null=True)
    mapping_type=models.ForeignKey(Dropdown,null=True,on_delete=models.SET_NULL,related_name='subject_type_map')

class SubjectTeacherMapping(BaseModel):
    subject = models.ForeignKey(SubjectMapping,on_delete=models.SET_NULL,null=True,related_name='identify_mapped_subjects')
    faculty = models.ForeignKey(Faculty,on_delete=models.SET_NULL,null=True)
    mapping_type=models.ForeignKey(Dropdown,null=True,on_delete=models.SET_NULL,related_name='sub_faculty')
# class Mappings(BaseModel):
#     course = models.ForeignKey(Dropdown,on_delete=models.SET_NULL, null=True,related_name='course_identification')
#     department=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='department_identification')
#     dept_mapping = models.ForeignKey("Mappings",on_delete=models.CASCADE,null=True,related_name='course_dept_mapping')
#     year = models.PositiveIntegerField(null=True)
#     subject = models.ForeignKey(Subject,on_delete=models.SET_NULL, null=True)
#     subj_mapping = models.ForeignKey("Mappings",on_delete=models.SET_NULL,null=True,related_name='dept_subj_mapping')
#     faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True   )
#     tr_mapping = models.ForeignKey("Mappings",on_delete=models.SET_NULL,null=True,related_name='tr_subj_mapping')
    
    