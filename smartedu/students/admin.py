from django.contrib import admin

# Register your models here.
from django.contrib import admin
from students.models import Standard, Section, Student


@admin.register(Standard)
class StandardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'standard')
   


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'standard', 'section', 'roll_number')
  