import pytest
from unittest.mock import patch, Mock
from user_request import UserAsk
from json_add_vac import JSONVacancy
import os

@pytest.fixture
def test_file():
    filename = "test_main_vacancies.json"
    yield filename
    if os.path.exists(filename):
        os.remove(filename)

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

class TestUserAsk:
    @patch('requests.get')
    def test_fetch_vacancies_from_hh(self, mock_get, mock_hh_response, test_file):
        # Настраиваем мок для API запроса
        mock_response = Mock()
        mock_response.json.return_value = mock_hh_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        user_ask = UserAsk(test_file)
        vacancies = user_ask.fetch_vacancies_from_hh("Python", 1)
        
        # Проверяем, что вакансии были найдены и сохранены
        json_manager = JSONVacancy(test_file)
        saved_vacancies = json_manager.get_vacancies(lambda v: True)
        assert len(saved_vacancies) == 2
        assert all("Python" in v["name"] for v in saved_vacancies)

    def test_search_and_sort_vacancies(self, test_file):
        user_ask = UserAsk(test_file)
        
        # Добавляем тестовые вакансии
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
        
        # Тестируем поиск Python вакансий
        python_vacancies = user_ask.search_vac("Python")
        assert len(python_vacancies) == 2
        
        # Проверяем сортировку по зарплате
        top_vacancies = user_ask.top_salary(2)
        assert len(top_vacancies) == 2
        assert top_vacancies[0]["salary"] == 200000
        assert top_vacancies[1]["salary"] == 180000

    @patch('requests.get')
    def test_error_handling(self, mock_get, test_file):
        # Тестируем обработку ошибок API
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        user_ask = UserAsk(test_file)
        vacancies = user_ask.fetch_vacancies_from_hh("NonExistent", 1)
        
        # Проверяем, что при ошибке API не было сохранено никаких вакансий
        json_manager = JSONVacancy(test_file)
        saved_vacancies = json_manager.get_vacancies(lambda v: True)
        assert len(saved_vacancies) == 0
