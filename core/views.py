# core/views.py
from django.shortcuts import render
from .models import Student, Discipline

def student_count_view(request):
    form_of_study = request.GET.get('form', 'дневная')
    count = Student.objects.filter(form_of_study=form_of_study).count()
    context = {
        'form': form_of_study,
        'count': count,
        'all_forms': [choice[0] for choice in Student.FORM_OF_STUDY_CHOICES]
    }
    return render(request, 'core/student_count.html', context)

def discipline_info_view(request):
    discipline_name = request.GET.get('name')
    discipline = None
    if discipline_name:
        discipline = Discipline.objects.filter(name__iexact=discipline_name).first()
    context = {
        'discipline': discipline,
        'discipline_name': discipline_name
    }
    return render(request, 'core/discipline_info.html', context)