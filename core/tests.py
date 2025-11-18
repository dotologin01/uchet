from django.test import TestCase, Client
from django.urls import reverse
from .models import Student, Discipline

# --- Юнит-тесты для моделей ---

class ModelTests(TestCase):

    def test_student_model_str(self):
        """Юнит-тест: Проверяем строковое представление модели Student."""
        student = Student.objects.create(
            last_name="Иванов",
            first_name="Иван",
            admission_year=2023,
            form_of_study="дневная",
            group_name="ИТ-101"
        )
        self.assertEqual(str(student), "Иванов Иван")

    def test_discipline_model_str(self):
        """Юнит-тест: Проверяем строковое представление модели Discipline."""
        discipline = Discipline.objects.create(
            name="Основы программирования",
            specialty="Информационные технологии",
            semester=1,
            hours=72,
            report_form="экзамен"
        )
        self.assertEqual(str(discipline), "Основы программирования")


# --- Интеграционные тесты для представлений (views) ---

class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        # Создаем студентов для проверки логики подсчета
        Student.objects.create(last_name="Петров", first_name="Петр", admission_year=2022, form_of_study="дневная", group_name="ИТ-201")
        Student.objects.create(last_name="Сидоров", first_name="Сидор", admission_year=2022, form_of_study="дневная", group_name="ИТ-201")
        Student.objects.create(last_name="Кузнецов", first_name="Кузьма", admission_year=2022, form_of_study="заочная", group_name="ИТ-202з")
        
        # Создаем дисциплину для проверки поиска
        self.discipline = Discipline.objects.create(name="Базы данных", specialty="ИТ", semester=3, hours=108, report_form="экзамен")

    def test_student_count_view_loads(self):
        """Интеграционный тест: Проверяем, что страница подсчета студентов загружается."""
        response = self.client.get(reverse('student_count'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/student_count.html')
        self.assertContains(response, "Подсчет студентов")

    def test_student_count_view_logic(self):
        """Интеграционный тест: Проверяем логику фильтрации на странице подсчета."""
        # Проверяем подсчет для дневной формы (должно быть 2)
        response_dnevnaya = self.client.get(reverse('student_count') + '?form=дневная')
        self.assertEqual(response_dnevnaya.context['count'], 2)

        # Проверяем подсчет для заочной формы (должно быть 1)
        response_zaochnaya = self.client.get(reverse('student_count') + '?form=заочная')
        self.assertEqual(response_zaochnaya.context['count'], 1)

        # Проверяем общее количество (должно быть 3)
        self.assertEqual(response_dnevnaya.context['total_count'], 3)

    def test_discipline_info_view_found(self):
        """Интеграционный тест: Проверяем поиск существующей дисциплины."""
        url = reverse('discipline_info') + f'?name={self.discipline.name}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/discipline_info.html')
        self.assertContains(response, "Информация о дисциплине")
        self.assertContains(response, self.discipline.name)
        self.assertContains(response, str(self.discipline.hours)) # Проверяем, что данные дисциплины есть на странице

    def test_discipline_info_view_not_found(self):
        """Интеграционный тест: Проверяем поиск несуществующей дисциплины."""
        url = reverse('discipline_info') + '?name=НесуществующаяДисциплина'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "не найдена")
        self.assertIsNone(response.context['discipline']) # Проверяем, что в контексте нет объекта

    