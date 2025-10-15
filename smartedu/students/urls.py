from django.urls import path
from students.views import StudentRegistrationView,ParentStudentLinkView
from students.views import StandardlistCreateView
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
    path("register/",views.StudentRegistrationView.as_view(), name="student-register"),
        path("link-parent/",views.ParentStudentLinkView.as_view(), name="link-parent"),
        path("standards/", views.StandardlistCreateView.as_view(), name="standard-list-create"),
    path("sections/", views.SectionListCreateView.as_view(), name="section-list-create"),
    path("attendance/mark/",csrf_exempt(views.AttendanceMarkView.as_view()),name="AttendanceMarkView"),
    path("attendance/student/<int:student_id>/",views.StudentAttendanceView.as_view(),name="StudentAttendanceView"),
    path("attendance/class/<int:class_id>/",views.ClassAttendanceView.as_view(),name="ClassAttendanceView"),
    path("class/<int:section_id>/",views.ClassAttendanceView.as_view(), name="ClassAttendanceShortView"),
    path("attendance-report/principal/", views.AttendanceReportPrincipalView.as_view(), name="attendance_report_principal"),
    path("attendance/parent/",views.AttendenceReoprtParentView.as_view(),name="AttendenceReoprtParentView"),
   
]
