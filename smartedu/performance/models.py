from django.db import models
from accounts.models import User
from students.models import Student,Standard,Section,Subject

# Create your models here.
class Exam(models.Model):
    name=models.CharField(max_length=100)
    date=models.DateField()
    standard=models.ForeignKey(Standard,on_delete=models.CASCADE)
    section=models.ForeignKey(Section,on_delete=models.CASCADE)
    created_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def _str_(self):
        return f"{self.name} - {self.standard.name} {self.section.name}"


class Mark(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)
    grade = models.CharField(max_length=3, blank=True, null=True)
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):

        if self.marks_obtained > self.max_marks:
            raise ValueError("Marks obtained cannot exceed max marks.")

        
        percentage = (self.marks_obtained / self.max_marks) * 100

        if percentage >= 90:
            self.grade = "A+"
        elif percentage >= 75:
            self.grade = "A"
        elif percentage >= 60:
            self.grade = "B"
        elif percentage >= 45:
            self.grade = "C"
        else:
            self.grade = "D"

        super().save(*args, **kwargs)