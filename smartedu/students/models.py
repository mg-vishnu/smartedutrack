

# Create your models here.
from django.db import models
from django.conf import settings 
from accounts.models import User 


class Standard(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):   
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=5)
    standard = models.ForeignKey(
        Standard, on_delete=models.CASCADE, related_name="sections"
    )

    def __str__(self):  
        return f"{self.standard.name} - {self.name}"


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,
        related_name="student_profile"
    )
    standard = models.ForeignKey(
        Standard, on_delete=models.SET_NULL, null=True, blank=True
    )
    section = models.ForeignKey(
        Section, on_delete=models.SET_NULL, null=True, blank=True
    )
    roll_number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.user.username} ({self.standard} - {self.section})"
    

class ParentStudent(models.Model):
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="children")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="parents")

    def __str__(self):
        return f"{self.parent.get_full_name()} - {self.student.user.get_full_name()}"









class Attendance(models.Model):
    student = models.ForeignKey(
        User , on_delete=models.CASCADE,
        limit_choices_to={"role":"STUDENT"},
        related_name="attendances"
    )
    date = models.DateField()
    status = models.CharField(max_length=20,choices=[("PRESENT","present"),("ABSENT","absent")])
    marked_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="attendance_marked")

    def __str__(self):
        return f"{self.student.username} - {self.date} - {self.status}"


class Subject(models.Model):
    name=models.CharField(max_length=100)
    code=models.CharField(max_length=30,unique=True)
    standard=models.ForeignKey(Standard,on_delete=models.CASCADE,related_name="subjects")
    teacher=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return f"{self.name} ({self.standard.name})"

