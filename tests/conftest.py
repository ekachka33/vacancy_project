import os
import sys
import pytest
from typing import Dict, Any
from unittest.mock import Mock

# Добавляем корневую директорию проекта в sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

@pytest.fixture
def test_vacancy_data() -> Dict[str, Any]:
    """Фикстура с тестовыми данными вакансии"""
    return {
        "id": "1",
        "name": "Python Developer",
        "alternate_url": "https://test.com/1",
        "salary": 150000,
        "description": "Python, Django required"
    }

@pytest.fixture
def test_file(tmp_path) -> str:
    """Фикстура для создания временного тестового файла"""
    filename = tmp_path / "test_vacancies.json"
    yield str(filename)
    if os.path.exists(filename):
        os.remove(filename)

@pytest.fixture
def mock_hh_response() -> Dict[str, Any]:
    """Фикстура с моком ответа API HeadHunter"""
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

@pytest.fixture
def mock_requests_get(monkeypatch, mock_hh_response):
    """Фикстура для мока requests.get"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_hh_response
    
    def mock_get(*args, **kwargs):
        return mock_response
    
    monkeypatch.setattr("requests.get", mock_get)
    return mock_get

@pytest.fixture
def multiple_test_vacancies() -> list:
    """Фикстура с набором тестовых вакансий для тестирования сортировки и фильтрации"""
    return [
        {
            "id": "1",
            "name": "Senior Python Developer",
            "alternate_url": "https://test.com/1",
            "salary": 200000,
            "description": "Python, Django, Senior level"
        },
        {
            "id": "2",
            "name": "Java Developer",
            "alternate_url": "https://test.com/2",
            "salary": 180000,
            "description": "Java, Spring"
        },
        {
            "id": "3",
            "name": "Junior Python Developer",
            "alternate_url": "https://test.com/3",
            "salary": 80000,
            "description": "Python basics"
        },
        {
            "id": "4",
            "name": "Data Scientist",
            "alternate_url": "https://test.com/4",
            "salary": 250000,
            "description": "Python, ML, Statistics"
        }
    ]
