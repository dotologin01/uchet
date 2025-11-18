# core/admin.py
from django.contrib import admin
from .models import Student, Discipline, Grade

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'group_name', 'form_of_study')
    search_fields = ('last_name', 'group_name', 'first_name') 

@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('name', 'semester', 'hours', 'report_form')
    list_filter = ('report_form', 'semester')
    search_fields = ('name',) 

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'discipline', 'grade', 'semester')
    autocomplete_fields = ('student', 'discipline')