from django.urls import path
from EduExam import views

urlpatterns = [
    path('examtype/',views.exam_type),
    path('examinfo/',views.exam_info),
    path('question_paper/',views.question_paper),
    path('paper_response/',views.paper_response),
    path('paper_evaluation/',views.paper_evaluation),
    path('exam_mapping/',views.exam_mapping),
    path('department_course/',views.department_course),
    path('subject_year/',views.subject_year),
    path('access_question/',views.access_question),
    path('get_question_paper/',views.get_question_paper),
    path('datesheet_mapping/',views.datesheet_maping),
    path('course_dept_mapping/',views.course_dept_mapping),
    path('all_exam_mapping/', views.all_exam_mapping),
    path('conduct_datesheet/', views.conduct_datesheet),
    path('get_exam_mapping/', views.get_exam_mapping),
    path('show_exam_type/', views.show_exam_type),
    path('select_sub/',views.select_sub),
    path('get_student_response/', views.get_student_response),
    path('get_question_answer/',views.get_question_answer),
    path('selectdept/', views.selectdept),
    path('get_shift_time/',views.get_shift_time),
    path('get_date/',views.get_date),
    path('datesheet/',views.datesheet),
    path('graph_course_dept/',views.graph_course_dept),
    path('select_paper_set/',views.select_paper_set),
    path('get_students_answer/',views.get_students_answer),
    path('paper_set/',views.paper_sets),
    path('subject_mapped_dept/',views.subject_mapped_dept),
    path('student_marks/', views.student_marks),
    path('exam_type_for_marks/',views.exam_type_for_marks),
    path('get_datesheet/',views.get_datesheet),
    path('view_paper/', views.view_paper),
    path('exam_type_for_marks/',views.exam_type_for_marks),
    path('publish_datesheet/',views.publish_datesheet),
    path('show_examtype_to_student/',views.show_examtype_to_student),
    path('show_datesheet/',views.show_datesheet)

  
    
]   