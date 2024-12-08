import unittest
import json
import os
from unittest.mock import Mock, patch
from user_request import UserAsk
from HH import HH
from CV import Sort_Vacan

class TestUserAsk(unittest.TestCase):
    """Тесты для класса UserAsk"""
    
    def setUp(self):
        self.test_file = "test_vacancies.json"
        self.user_ask = UserAsk(self.test_file)
        self.test_vacancy = {
            "id": "test1",
            "name": "Python Developer",
            "url": "https://test.com",
            "salary": 100000,
            "description": "Test description"
        }

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_vacancy(self):
        """Тест добавления вакансии"""
        self.user_ask.add_vacancy(self.test_vacancy)
        with open(self.test_file, 'r') as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], "test1")

    def test_search_vac(self):
        """Тест поиска вакансии"""
        self.user_ask.add_vacancy(self.test_vacancy)
        results = self.user_ask.search_vac("Python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Python Developer")

    def test_delete_vacancy(self):
        """Тест удаления вакансии"""
        self.user_ask.add_vacancy(self.test_vacancy)
        result = self.user_ask.delete_vacancy("test1")
        self.assertTrue(result)
        with open(self.test_file, 'r') as f:
            data = json.load(f)
        self.assertEqual(len(data), 0)

    def test_top_salary(self):
        """Тест сортировки по зарплате"""
        vacancies = [
            {
                "id": "1",
                "name": "Dev 1",
                "url": "https://test.com",
                "salary": 100000,
                "description": "Test"
            },
            {
                "id": "2",
                "name": "Dev 2",
                "url": "https://test.com",
                "salary": 200000,
                "description": "Test"
            }
        ]
        for vac in vacancies:
            self.user_ask.add_vacancy(vac)
        
        top = self.user_ask.top_salary(1)
        self.assertEqual(len(top), 1)
        self.assertEqual(top[0]["salary"], 200000)


class TestHH(unittest.TestCase):
    """Тесты для класса HH"""
    
    def setUp(self):
        self.mock_file_worker = Mock()
        self.hh = HH(self.mock_file_worker)

    def test_parse_salary(self):
        """Тест парсинга зарплаты"""
        # Тест с полными данными о зарплате
        salary_data = {"from": 100000, "to": 150000}
        self.assertEqual(self.hh._parse_salary(salary_data), 100000)

        # Тест без минимальной зарплаты
        salary_data = {"from": None, "to": 150000}
        self.assertEqual(self.hh._parse_salary(salary_data), 150000)

        # Тест с пустыми данными
        self.assertEqual(self.hh._parse_salary(None), 0)

    @patch('requests.get')
    def test_load_vacancies(self, mock_get):
        """Тест загрузки вакансий"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [{
                'id': '1',
                'name': 'Python Developer',
                'alternate_url': 'https://hh.ru/vacancy/1',
                'salary': {'from': 100000, 'to': 150000},
                'snippet': {'requirement': 'Python experience'}
            }]
        }
        mock_get.return_value = mock_response

        vacancies = self.hh.load_vacancies("Python", 1)
        
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]['name'], 'Python Developer')
        self.mock_file_worker.add_vacancy.assert_called_once()

    def test_add_vac(self):
        """Тест добавления вакансии через API"""
        vacancy = {
            "id": "1",
            "name": "Test Vacancy",
            "url": "https://test.com",
            "salary": 100000,
            "description": "Test description"
        }
        self.hh.add_vac(vacancy)
        self.mock_file_worker.add_vacancy.assert_called_once_with(vacancy)

    def test_del_vac(self):
        """Тест удаления вакансии через API"""
        self.hh.del_vac("1")
        self.mock_file_worker.delete_vacancy.assert_called_once_with("1")


class TestSortVacan(unittest.TestCase):
    """Тесты для класса Sort_Vacan"""
    
    def setUp(self):
        self.vacancy = Sort_Vacan(
            name="Python Developer",
            url="https://test.com",
            salary=100000,
            description="Test description"
        )

    def test_initialization(self):
        """Тест инициализации объекта вакансии"""
        self.assertEqual(self.vacancy.name, "Python Developer")
        self.assertEqual(self.vacancy.salary, 100000)
        self.assertIsNotNone(self.vacancy.id)

    def test_validation(self):
        """Тест валидации данных"""
        # Тест с невалидной зарплатой
        vacancy = Sort_Vacan(
            name="Test",
            url="https://test.com",
            salary="invalid",
            description="Test"
        )
        self.assertEqual(vacancy.salary, 0)

        # Тест с пустым описанием
        vacancy = Sort_Vacan(
            name="Test",
            url="https://test.com",
            salary=100000,
            description=""
        )
        self.assertEqual(vacancy.description, "Описание не указано")

    def test_comparison(self):
        """Тест сравнения вакансий"""
        vacancy1 = Sort_Vacan(
            name="Dev 1",
            url="https://test.com",
            salary=100000,
            description="Test"
        )
        vacancy2 = Sort_Vacan(
            name="Dev 2",
            url="https://test.com",
            salary=200000,
            description="Test"
        )

        self.assertTrue(vacancy1 < vacancy2)
        self.assertTrue(vacancy2 > vacancy1)
        self.assertFalse(vacancy1 == vacancy2)

    def test_to_dict(self):
        """Тест преобразования в словарь"""
        vacancy_dict = self.vacancy.to_dict()
        self.assertEqual(vacancy_dict["name"], "Python Developer")
        self.assertEqual(vacancy_dict["salary"], 100000)
        self.assertIn("id", vacancy_dict)

    def test_from_dict(self):
        """Тест создания объекта из словаря"""
        data = {
            "id": "test-id",
            "name": "Python Developer",
            "url": "https://test.com",
            "salary": 100000,
            "description": "Test description"
        }
        vacancy = Sort_Vacan.from_dict(data)
        self.assertEqual(vacancy.name, "Python Developer")
        self.assertEqual(vacancy.salary, 100000)
        self.assertEqual(vacancy.id, "test-id")


if __name__ == '__main__':
    unittest.main()
