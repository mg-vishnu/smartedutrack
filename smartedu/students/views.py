from django.shortcuts import render
import json

# Create your views here.
from rest_framework import generics, permissions
from students.serializers import StudentRegistrationSerializer,LinkParentSerializer,StandardSerializer, SectionSerializer , AttendanceDailySerializer
from students.models import Student,ParentStudent
from rest_framework import generics
from .models import Standard, Section



class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "role", None) == "teacher"


class StudentRegistrationView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentRegistrationSerializer
    permission_classes=[IsTeacher]

class ParentStudentLinkView(generics.CreateAPIView):
    queryset = ParentStudent.objects.all()
    serializer_class = LinkParentSerializer
    permission_classes = [IsTeacher]



class StandardlistCreateView(generics.ListCreateAPIView):
    queryset=Standard.objects.all()
    serializer_class= StandardSerializer
    permission_classes=[IsTeacher]

class SectionListCreateView(generics.ListCreateAPIView):
    queryset=Section.objects.all()
    serializer_class= SectionSerializer
    permission_classes=[IsTeacher]


from rest_framework import generics, status 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from students.models import Attendance, User 
from students.serializers import AttendanceMarkSerializer, AttendanceSerializer 


class AttendanceMarkView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceMarkSerializer
    permission_classes = []


    def post(self,request,*args,**kwargs):
        json_data=request.data
        py_data=json.loads(json_data)

        many = isinstance(py_data,list)
        serializer = self.get_serializer(data=py_data,many=many)
        serializer.is_valid(raise_exception = True)
        records =[]

        if type(serializer.validated_data)==list:
            for item in serializer.validated_data:
                student_id = int(item["student_id"])
                
                date = item['date']
                status_ = item['status']

                attendance = Attendance.objects.filter(student_id=student_id,date=date).first()
                teacher=User.objects.get(id=3)
                if attendance:
                    attendance.status = status_
                    attendance.marked_by = teacher
                    attendance.save()
                else:
                    Attendance.objects.create(
                        student_id=student_id,
                        date=date,
                        status=status_,
                        marked_by = teacher
                    )
                request.append(obj)
        else:
            obj,created = Attendance.objects.update_or_create(
                student_id = int(serializer.validated_data["student_id"]),
                date = serializer.validated_data['date'],
                defaults = {"status":serializer.validated_data["status"],"marked_by":request.user})
            records.append(obj)
        return Response(AttendanceSerializer(records, many = True).data, status = status.HTTP_200_OK)
    
class StudentAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        student_id = self.kwargs["student_id"]


        if self.request.user.role == "STUDENT" and self.request.user.id != int(student_id):
            return Attendance.objects.none()
        
        return Attendance.objects.filter(student_id=student_id).order_by("-date")
    
class ClassAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    # permission_classes = [IsTeacher,IsAuthenticated]

    def get_queryset(self):
        class_id = self.kwargs["class_id"]
        
        date = self.request.query_params.get("date")
        queryset=Attendance.objects.all()
       

        if date:
            queryset=queryset.filter(data=data)
        return queryset
           

      


def calculate_percentage(present, total_days):
    if total_days == 0:
        return "0%"
    return f"{round((present / total_days) * 100, 2)}%"


class AttendanceReportPrincipalView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
       
        queryset = Attendance.objects.select_related(
            "student__student_profile__standard",
            "student__student_profile__section"
        )

        
        standard = request.query_params.get("standard")
        section = request.query_params.get("section")
        from_date = request.query_params.get("from_date")
        to_date = request.query_params.get("to_date")

        if standard:
            queryset = queryset.filter(student__student_profile__standard_id=standard)

        if section:
            queryset = queryset.filter(student__student_profile__section_id=section)

        if from_date and to_date:
            queryset = queryset.filter(date__range=[from_date, to_date])

      
        summary_data = []
        student_ids = queryset.values_list("student_id", flat=True).distinct()

        for sid in student_ids:
            student_records = queryset.filter(student_id=sid)
            if not student_records.exists():
                continue

           
            student_profile = student_records.first().student.student_profile

            total_days = student_records.count()
            total_present = student_records.filter(status="Present").count()
            total_absent = student_records.filter(status="Absent").count()

            summary_data.append({
                "student_name": student_profile.user.get_full_name(),
                "standard": student_profile.standard.name,
                "section": student_profile.section.name,
                "total_present": total_present,
                "total_absent": total_absent,
                "attendance_percentage": calculate_percentage(total_present, total_days)
            })

       
        total_students = len(student_ids)
        total_days = queryset.values("date").distinct().count()
        overall_present = queryset.filter(status="Present").count()
        overall_percentage = calculate_percentage(overall_present, queryset.count())

        return Response({
            "summary": {
                "total_students": total_students,
                "total_days": total_days,
                "average_attendance": overall_percentage
            },
            "records": summary_data
        })

class AttendenceReoprtParentView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        parent = request.user   

        
        linked_students = [ps.student for ps in ParentStudent.objects.filter(parent=parent)]

        from_date = request.query_params.get("from_date")
        to_date = request.query_params.get("to_date")

        data = []
        for student_ in linked_students:
            student_user = student_.user   

           
            user_records = Attendance.objects.filter(student=student_user)

            if from_date and to_date:
                user_records = user_records.filter(date__range=[from_date, to_date])

            if not user_records.exists():
                continue

            total_days = user_records.count()
            total_present = user_records.filter(status="PRESENT").count()
            total_absent = user_records.filter(status="ABSENT").count()

            child_data = {
                "student_name": f"{student_user.first_name} {student_user.last_name}",
                "standard": student_.standard.name if student_.standard else None,
                "section": student_.section.name if student_.section else None,
                "summary": {
                    "total_days": total_days,
                    "present": total_present,
                    "absent": total_absent,
                    "percentage": calculate_percentage(total_present, total_days),
                },
                "records": AttendanceDailySerializer(user_records, many=True).data,
            }
            data.append(child_data)

        return Response({"children": data})
