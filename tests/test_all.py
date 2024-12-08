import pytest
import json
import os
import requests
from unittest.mock import Mock, patch
from CV import Sort_Vacan
from HH import HH
from user_request import UserAsk
from json_add_vac import JSONFileManager

# === Фикстуры ===
@pytest.fixture
def test_file():
    filename = "test_vacancies.json"
    yield filename
    if os.path.exists(filename):
        os.remove(filename)

@pytest.fixture
def test_vacancy():
    return Sort_Vacan(
        name="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary=150000,
        description="Python developer position"
    )

@pytest.fixture
def sample_vacancy():
    return {
        "id": "1",
        "name": "Python Developer",
        "url": "https://test.com/1",
        "salary": 150000,
        "description": "Python, Django required"
    }

@pytest.fixture
def mock_hh_response():
    return {
        "items": [
            {
                "id": "1",
                "name": "Senior Python Developer",
                "alternate_url": "https://hh.ru/vacancy/123",
                "salary": {"from": 200000, "to": 300000},
                "snippet": {
                    "requirement": "Python, Django, PostgreSQL",
                    "responsibility": "Development and maintenance"
                }
            },
            {
                "id": "2",
                "name": "Middle Python Developer",
                "alternate_url": "https://hh.ru/vacancy/456",
                "salary": {"from": 150000, "to": 200000},
                "snippet": {
                    "requirement": "Python, Flask",
                    "responsibility": "Backend development"
                }
            }
        ]
    }

# === Тесты Sort_Vacan ===
class TestSortVacan:
    def test_vacancy_creation(self, test_vacancy):
        assert test_vacancy.name == "Python Developer"
        assert test_vacancy.salary == 150000
        assert test_vacancy.id is not None

    def test_vacancy_validation(self):
        vacancy = Sort_Vacan(
            name="Test",
            url="",
            salary="invalid",
            description=""
        )
        assert vacancy.salary == 0
        assert vacancy.url == "#"
        assert vacancy.description == "Описание не указано"

    def test_vacancy_comparison(self, test_vacancy):
        other_vacancy = Sort_Vacan(
            name="Other",
            url="https://hh.ru/vacancy/456",
            salary=100000,
            description="Other position"
        )
        assert test_vacancy > other_vacancy
        assert other_vacancy < test_vacancy
        assert not test_vacancy == other_vacancy

# === Тесты Vacancy ===
class TestVacancy:
    def test_add_vacancy(self, test_file):
        user_ask = UserAsk(test_file)
        vacancy_data = {
            "id": "123",
            "name": "Test Vacancy",
            "url": "https://test.com",
            "salary": 100000,
            "description": "Test description"
        }
        user_ask.add_vacancy(vacancy_data)
        
        with open(test_file, 'r') as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["name"] == "Test Vacancy"

    def test_get_vacancies(self, test_file):
        user_ask = UserAsk(test_file)
        vacancy_data = {
            "id": "123",
            "name": "Python Developer",
            "url": "https://test.com",
            "salary": 100000,
            "description": "Python required"
        }
        user_ask.add_vacancy(vacancy_data)
        
        python_vacancies = user_ask.get_vacancies(
            lambda v: "Python" in v["name"] or "Python" in v["description"]
        )
        assert len(python_vacancies) == 1

    def test_delete_vacancy(self, test_file):
        user_ask = UserAsk(test_file)
        vacancy_data = {
            "id": "123",
            "name": "Test Vacancy",
            "url": "https://test.com",
            "salary": 100000,
            "description": "Test description"
        }
        user_ask.add_vacancy(vacancy_data)
        assert user_ask.delete_vacancy("123") is True
        assert user_ask.delete_vacancy("456") is False

# === Тесты JSONFileManager ===
class TestJSONFileManager:
    def test_add_vacancy(self, test_file, sample_vacancy):
        manager = JSONFileManager(test_file)
        manager.add_vacancy(sample_vacancy)
        
        assert os.path.exists(test_file)
        with open(test_file, 'r') as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["name"] == "Python Developer"
        assert data[0]["description"] == "Python, Django required"

    def test_get_vacancies(self, test_file, sample_vacancy):
        manager = JSONFileManager(test_file)
        manager.add_vacancy(sample_vacancy)
        
        java_vacancy = {
            "id": "2",
            "name": "Java Developer",
            "url": "https://test.com/2",
            "salary": 160000,
            "description": "Java required"
        }
        manager.add_vacancy(java_vacancy)
        
        python_vacancies = manager.get_vacancies(
            lambda v: "Python" in v["name"] or "Python" in v["description"]
        )
        assert len(python_vacancies) == 1
        assert python_vacancies[0]["name"] == "Python Developer"

    def test_delete_vacancy(self, test_file, sample_vacancy):
        manager = JSONFileManager(test_file)
        manager.add_vacancy(sample_vacancy)
        
        manager.delete_vacancy("1")
        
        with open(test_file, 'r') as f:
            data = json.load(f)
        assert len(data) == 0

    def test_get_vacancies_empty_file(self, test_file):
        manager = JSONFileManager(test_file)
        vacancies = manager.get_vacancies(lambda v: True)
        assert len(vacancies) == 0

# === Тесты UserAsk ===
class TestUserAsk:
    @patch('requests.get')
    def test_fetch_vacancies_from_hh(self, mock_get, mock_hh_response, test_file):
        mock_response = Mock()
        mock_response.json.return_value = mock_hh_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        user_ask = UserAsk(test_file)
        vacancies = user_ask.fetch_vacancies_from_hh("Python", 1)
        
        json_manager = JSONFileManager(test_file)
        saved_vacancies = json_manager.get_vacancies(lambda v: True)
        assert len(saved_vacancies) == 2
        assert all("Python" in v["name"] for v in saved_vacancies)

    def test_search_and_sort_vacancies(self, test_file):
        user_ask = UserAsk(test_file)
        
        vacancies = [
            {
                "id": "1",
                "name": "Senior Python Developer",
                "url": "https://test.com/1",
                "salary": 200000,
                "description": "Python, Django required"
            },
            {
                "id": "2",
                "name": "Java Developer",
                "url": "https://test.com/2",
                "salary": 180000,
                "description": "Java required"
            },
            {
                "id": "3",
                "name": "Junior Python Developer",
                "url": "https://test.com/3",
                "salary": 120000,
                "description": "Python basics"
            }
        ]
        
        for v in vacancies:
            user_ask.add_vacancy(v)
        
        python_vacancies = user_ask.search_vac("Python")
        assert len(python_vacancies) == 2
        
        top_vacancies = user_ask.top_salary(2)
        assert len(top_vacancies) == 2
        assert top_vacancies[0]["salary"] == 200000
        assert top_vacancies[1]["salary"] == 180000

    @patch('requests.get')
    def test_error_handling(self, mock_get, test_file):
        # Настраиваем мок для имитации ошибки API
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"items": []}  # Добавляем пустой список items
        mock_get.return_value = mock_response
        
        user_ask = UserAsk(test_file)
        vacancies = user_ask.fetch_vacancies_from_hh("NonExistent", 1)
        
        json_manager = JSONFileManager(test_file)
        saved_vacancies = json_manager.get_vacancies(lambda v: True)
        assert len(saved_vacancies) == 0

# === Тесты HH ===
class TestHH:
    @patch('requests.get')
    def test_get_vacancies_by_keyword(self, mock_get, mock_hh_response, test_file):
        mock_response = Mock()
        mock_response.json.return_value = mock_hh_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        user_ask = UserAsk(test_file)
        hh = HH(user_ask)
        
        vacancies = hh.get_vacancies_by_keyword("Python")
        assert len(vacancies) > 0
        assert "Python" in vacancies[0]["name"]

    @patch('requests.get')
    def test_api_error_handling(self, mock_get, test_file):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        user_ask = UserAsk(test_file)
        hh = HH(user_ask)
        
        vacancies = hh.get_vacancies_by_keyword("NonExistentKeyword")
        assert len(vacancies) == 0

    def test_add_vac(self, test_file):
        user_ask = UserAsk(test_file)
        hh = HH(user_ask)
        
        vacancy_data = {
            "id": "test_id",  
            "name": "Test Vacancy",
            "alternate_url": "https://test.com",  
            "salary": {"from": 100000, "to": 150000},
            "snippet": {"requirement": "Python", "responsibility": "Development"}
        }
        
        hh.add_vac(vacancy_data)
        saved_vacancies = user_ask.get_vacancies(lambda v: True)
        assert len(saved_vacancies) == 1
        assert saved_vacancies[0]["name"] == "Test Vacancy"

    def test_get_vac(self, test_file):
        user_ask = UserAsk(test_file)
        hh = HH(user_ask)
        
        vacancy_data = {
            "id": "test_id",  
            "name": "Python Developer",
            "alternate_url": "https://test.com",  
            "salary": {"from": 100000, "to": 150000},
            "snippet": {"requirement": "Python", "responsibility": "Development"}
        }
        hh.add_vac(vacancy_data)
        
        python_vacancies = hh.get_vac(lambda v: "Python" in v["name"])
        assert len(python_vacancies) == 1

# === Тесты Functionality ===
class TestFunctionality:
    @patch('requests.get')
    def test_full_workflow(self, mock_get, mock_hh_response, test_file):
        """Тест полного рабочего процесса: поиск, сохранение, фильтрация вакансий"""
        # Настраиваем мок для API
        mock_response = Mock()
        mock_response.json.return_value = mock_hh_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Инициализация
        user_ask = UserAsk(test_file)
        hh = HH(user_ask)
        
        # 1. Поиск вакансий
        vacancies = hh.get_vacancies_by_keyword("Python Developer")
        assert len(vacancies) > 0, "Должны быть найдены вакансии"
        
        # 2. Проверяем данные первой вакансии
        first_vacancy = vacancies[0]
        assert "name" in first_vacancy, "Вакансия должна содержать название"
        assert "alternate_url" in first_vacancy, "Вакансия должна содержать URL"
        
        # 3. Сохранение вакансии
        hh.add_vac(first_vacancy)
        
        # 4. Проверка чтения сохраненных вакансий
        saved_vacancies = user_ask.get_vacancies(lambda v: True)
        assert len(saved_vacancies) > 0, "Должна быть хотя бы одна сохраненная вакансия"
        
        # 5. Проверка фильтрации
        python_vacancies = user_ask.get_vacancies(lambda v: "Python" in v.get("name", ""))
        assert len(python_vacancies) > 0, "Должны найтись Python вакансии"
        
        # 6. Проверка сортировки по зарплате
        if len(saved_vacancies) > 1:
            sorted_vacancies = Sort_Vacan.sort_by_salary(saved_vacancies)
            assert len(sorted_vacancies) == len(saved_vacancies), "Количество вакансий после сортировки не должно измениться"
