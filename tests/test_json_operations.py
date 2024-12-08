import pytest
import json
import os
from json_add_vac import JSONVacancy

@pytest.fixture
def test_file():
    filename = "test_json_operations.json"
    yield filename
    if os.path.exists(filename):
        os.remove(filename)

@pytest.fixture
def sample_vacancy():
    return {
        "id": "1",
        "name": "Python Developer",
        "url": "https://test.com/1",
        "salary": 150000,
        "description": "Python, Django required"
    }

class TestJSONVacancy:
    def test_add_vacancy(self, test_file, sample_vacancy):
        # Тестируем добавление вакансии
        manager = JSONVacancy(test_file)
        manager.add_vacancy(sample_vacancy)
        
        # Проверяем, что файл создан и содержит правильные данные
        assert os.path.exists(test_file)
        with open(test_file, 'r') as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["name"] == "Python Developer"
        assert data[0]["requirement"] == "Python, Django required"

    def test_get_vacancies(self, test_file, sample_vacancy):
        # Создаем менеджер и добавляем тестовые вакансии
        manager = JSONVacancy(test_file)
        manager.add_vacancy(sample_vacancy)
        
        # Добавим еще одну вакансию
        java_vacancy = {
            "id": "2",
            "name": "Java Developer",
            "url": "https://test.com/2",
            "salary": 160000,
            "description": "Java required"
        }
        manager.add_vacancy(java_vacancy)
        
        # Тестируем поиск Python вакансий
        python_vacancies = manager.get_vacancies(
            lambda v: "Python" in v["name"] or "Python" in v["requirement"]
        )
        assert len(python_vacancies) == 1
        assert python_vacancies[0]["name"] == "Python Developer"

    def test_delete_vacancy(self, test_file, sample_vacancy):
        # Создаем менеджер и добавляем вакансию
        manager = JSONVacancy(test_file)
        manager.add_vacancy(sample_vacancy)
        
        # Удаляем вакансию
        manager.delete_vacancy("1")
        
        # Проверяем, что вакансия удалена
        with open(test_file, 'r') as f:
            data = json.load(f)
        assert len(data) == 0

    def test_get_vacancies_empty_file(self, test_file):
        # Тестируем получение вакансий из пустого файла
        manager = JSONVacancy(test_file)
        vacancies = manager.get_vacancies(lambda v: True)
        assert len(vacancies) == 0

    def test_get_vacancies_with_criteria(self, test_file, sample_vacancy):
        # Создаем менеджер и добавляем вакансию
        manager = JSONVacancy(test_file)
        manager.add_vacancy(sample_vacancy)
        
        # Тестируем поиск по зарплате
        high_salary_vacancies = manager.get_vacancies(
            lambda v: v["salary"] > 140000
        )
        assert len(high_salary_vacancies) == 1
        
        # Тестируем поиск по несуществующей зарплате
        low_salary_vacancies = manager.get_vacancies(
            lambda v: v["salary"] < 100000
        )
        assert len(low_salary_vacancies) == 0
