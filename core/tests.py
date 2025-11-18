# core/tests.py

from django.test import TestCase, Client
# ИСПРАВЛЕНИЕ 1: Добавляем resolve
from django.urls import reverse, resolve 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Student, Discipline
# ИСПРАВЛЕНИЕ 2: Импортируем наши view-функции
from .views import student_count_view, discipline_info_view

# --- Юнит-тесты для моделей (включая валидацию) ---
class ModelValidationTests(TestCase):
    def test_student_model_str(self):
        student = Student.objects.create(last_name="Иванов", first_name="Иван", admission_year=2023, form_of_study="дневная", group_name="ИТ-101")
        self.assertEqual(str(student), "Иванов Иван")
    def test_discipline_model_str(self):
        discipline = Discipline.objects.create(name="Основы программирования", specialty="Информационные технологии", semester=1, hours=72, report_form="экзамен")
        self.assertEqual(str(discipline), "Основы программирования")
    def test_student_creation_with_invalid_choice(self):
        with self.assertRaises(ValidationError):
            student = Student(last_name="Тестов", first_name="Тест", admission_year=2023, form_of_study="несуществующая", group_name="ИТ-101")
            student.full_clean()
    def test_student_creation_with_long_name(self):
        long_name = "А" * 101
        with self.assertRaises(ValidationError):
            student = Student(last_name=long_name, first_name="Тест", admission_year=2023, form_of_study="дневная", group_name="ИТ-101")
            student.full_clean()

# --- Интеграционные тесты для представлений (views) ---
class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        Student.objects.create(last_name="Петров", first_name="Петр", admission_year=2022, form_of_study="дневная", group_name="ИТ-201")
        Student.objects.create(last_name="Сидоров", first_name="Сидор", admission_year=2022, form_of_study="дневная", group_name="ИТ-201")
        Student.objects.create(last_name="Кузнецов", first_name="Кузьма", admission_year=2022, form_of_study="заочная", group_name="ИТ-202з")
        self.discipline = Discipline.objects.create(name="Базы данных", specialty="ИТ", semester=3, hours=108, report_form="экзамен")
    def test_student_count_view_loads(self):
        response = self.client.get(reverse('student_count'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/student_count.html')
    def test_student_count_view_logic(self):
        response_dnevnaya = self.client.get(reverse('student_count') + '?form=дневная')
        self.assertEqual(response_dnevnaya.context['count'], 2)
        response_zaochnaya = self.client.get(reverse('student_count') + '?form=заочная')
        self.assertEqual(response_zaochnaya.context['count'], 1)
    def test_discipline_info_view_found(self):
        response = self.client.get(reverse('discipline_info') + f'?name={self.discipline.name}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.discipline.name)
    def test_discipline_info_view_not_found(self):
        response = self.client.get(reverse('discipline_info') + '?name=НесуществующаяДисциплина')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "не найдена")

# --- Интеграционные тесты для Админ-панели ---
class AdminInterfaceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(username='testadmin', email='admin@test.com', password='password123') # nosec B106
        self.client.login(username='testadmin', password='password123') # nosec B106

    def test_add_student_successfully(self):
        add_url = reverse('admin:core_student_add')
        student_data = {'last_name': "О'Коннор", 'first_name': 'Сара', 'middle_name': 'Джейн', 'admission_year': 2024, 'form_of_study': 'вечерняя', 'group_name': 'В-303'}
        response = self.client.post(add_url, student_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Student.objects.filter(last_name="О'Коннор").exists())
        self.assertContains(response, "was added successfully")

    def test_add_student_with_invalid_data(self):
        add_url = reverse('admin:core_student_add')
        invalid_data = {'last_name': '', 'first_name': 'Джон', 'admission_year': 'не_число', 'form_of_study': 'дневная', 'group_name': 'Д-404'}
        response = self.client.post(add_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Student.objects.filter(first_name="Джон").exists())
        self.assertContains(response, 'This field is required.')

# --- Юнит-тесты для URL-роутинга ---
class URLTests(TestCase):
    def test_student_count_url_resolves(self):
        url = '/student-count/'
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, student_count_view)

    def test_discipline_info_url_resolves(self):
        url = '/discipline-info/'
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, discipline_info_view)

    def test_student_count_url_reverse(self):
        url_name = 'student_count'
        resolved_path = reverse(url_name)
        self.assertEqual(resolved_path, '/student-count/')

    def test_discipline_info_url_reverse(self):
        url_name = 'discipline_info'
        resolved_path = reverse(url_name)
        self.assertEqual(resolved_path, '/discipline-info/')