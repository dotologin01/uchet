# core/models.py
from django.db import models

class Student(models.Model):
    FORM_OF_STUDY_CHOICES = [
        ('дневная', 'Дневная'),
        ('вечерняя', 'Вечерняя'),
        ('заочная', 'Заочная'),
    ]
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    admission_year = models.IntegerField(verbose_name="Год поступления")
    form_of_study = models.CharField(max_length=20, choices=FORM_OF_STUDY_CHOICES, verbose_name="Форма обучения")
    group_name = models.CharField(max_length=50, verbose_name="Номер/название группы")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Discipline(models.Model):
    REPORT_FORM_CHOICES = [
        ('экзамен', 'Экзамен'),
        ('зачет', 'Зачет'),
    ]
    name = models.CharField(max_length=200, verbose_name="Название дисциплины")
    specialty = models.CharField(max_length=200, verbose_name="Название специальности")
    semester = models.IntegerField(verbose_name="Семестр")
    hours = models.IntegerField(verbose_name="Количество часов")
    report_form = models.CharField(max_length=20, choices=REPORT_FORM_CHOICES, verbose_name="Форма отчетности")

    def __str__(self):
        return self.name

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name="Дисциплина")
    year = models.IntegerField(verbose_name="Год")
    semester = models.IntegerField(verbose_name="Семестр")
    grade = models.CharField(max_length=50, verbose_name="Оценка")

    def __str__(self):
        return f"{self.student} - {self.discipline}: {self.grade}"