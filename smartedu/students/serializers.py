from rest_framework import serializers
from accounts.models import User

from students.models import Student, Standard, Section


from rest_framework import serializers
from students.models import Attendance
from students.models import ParentStudent
from .models import Student, Standard, Section

from rest_framework import serializers
from accounts.models import User
from students.models import Student

class StudentRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ["username", "email", "password", "roll_number", "standard", "section"]

    def create(self, validated_data):
        
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            username=username,
            email=email,
            role="STUDENT"
        )
        user.set_password(password)
        user.save()

     
        student = Student.objects.create(user=user, **validated_data)
        return student





class LinkParentSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(write_only=True)
    student_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ParentStudent
        fields = ["id", "parent_id", "student_id"]

    def validate(self, data):
        
        try:
            parent = User.objects.get(id=data["parent_id"], role="parent")
        except User.DoesNotExist:
            raise serializers.ValidationError({"parent_id": "Invalid parent_id or user is not a parent."})

        
        try:
            student = Student.objects.get(id=data["student_id"])
        except Student.DoesNotExist:
            raise serializers.ValidationError({"student_id": "Invalid student_id."})

    
        if ParentStudent.objects.filter(parent=parent, student=student).exists():
            raise serializers.ValidationError("This parent is already linked with the student.")

        return data

    def create(self, validated_data):
        parent = User.objects.get(id=validated_data["parent_id"])
        student = Student.objects.get(id=validated_data["student_id"])
        link,created=ParentStudent.objects.get_or_create(parent=parent,student=student)
        return link
    def to_representation(self, instance):
        return {
        "link_id": instance.id,
        "student": instance.student.user.first_name,
        "parent": instance.parent.first_name,
        "message": "parent linked to student successfully"
    }

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Section
        fields=["id","name","standard"]

class StandardSerializer(serializers.ModelSerializer):
    sections=SectionSerializer(many=True,read_only=True)

    class Meta:
        model=Standard
        fields=["id","name","sections"]



class StandardSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Standard
        fields = ["id", "name", "sections"]


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["id","student","date","status","marked_by"]
        read_only_fields = ["id","marked_by"]

class AttendanceMarkSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    date = serializers.DateField()
    status = serializers.ChoiceField(choices=[("PRESENT","present"),("ABSENT","absent")])


class AttendanceDailySerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(read_only=True)
    standard = serializers.CharField(read_only=True)
    section = serializers.CharField(read_only=True)

    class Meta:
        model = Attendance
        fields = ["date", "status", "student_name", "standard", "section"]


class AttendanceSummarySerializer(serializers.Serializer):
    student_name = serializers.CharField()
    standard = serializers.CharField()
    section = serializers.CharField()
    total_present = serializers.IntegerField()
    total_absent = serializers.IntegerField()
    attendance_percentage = serializers.CharField()


class AttendanceSummarySerializer(serializers.Serializer):
    student_name = serializers.CharField()
    standard = serializers.CharField()
    section = serializers.CharField()
    total_present = serializers.IntegerField()
    total_absent = serializers.IntegerField()
    attendance_percentage = serializers.CharField()