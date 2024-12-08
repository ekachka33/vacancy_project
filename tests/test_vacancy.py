import pytest
from CV import Sort_Vacan
from HH import HH
from user_request import UserAsk
import json
import os
import requests
from unittest.mock import Mock, patch

@pytest.fixture
def test_vacancy():
    return Sort_Vacan(
        name="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary=150000,
        description="Python developer position"
    )

@pytest.fixture
def test_file():
    filename = "test_vacancies.json"
    yield filename
    if os.path.exists(filename):
        os.remove(filename)

@pytest.fixture
def mock_hh_response():
    return {
        "items": [
            {
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/123",
                "salary": {"from": 150000, "to": 200000},
                "snippet": {"requirement": "Python, Django", "responsibility": "Development"}
            }
        ]
    }

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

class TestUserAsk:
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
            "name": "Python Developer",
            "alternate_url": "https://test.com",
            "salary": {"from": 100000, "to": 150000},
            "snippet": {"requirement": "Python", "responsibility": "Development"}
        }
        hh.add_vac(vacancy_data)
        
        python_vacancies = hh.get_vac(lambda v: "Python" in v["name"])
        assert len(python_vacancies) == 1
