vacancy_project/
├── README.md           # Документация проекта
├── requirements.txt    # Зависимости проекта
├── setup.py           # Файл для установки пакета
├── .gitignore         # Игнорируемые файлы для Git
├── main.py            # Основной файл программы
├── user_request.py    # Класс для работы с запросами пользователя
├── HH.py             # Класс для работы с API HeadHunter
├── CAPI.py           # Абстрактный класс для работы с API
├── CV.py             # Класс для работы с вакансиями
└── tests/            # Директория с тестами
    ├── __init__.py
    ├── test_user_request.py
    ├── test_hh.py
    └── test_cv.pyimport unittest
from unittest.mock import Mock, patch
from HH import HH

class TestHH(unittest.TestCase):
    def setUp(self):
        self.mock_file_worker = Mock()
        self.hh = HH(self.mock_file_worker)

    def test_parse_salary(self):
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
        # Мокаем ответ API
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
        self.hh.del_vac("1")
        self.mock_file_worker.delete_vacancy.assert_called_once_with("1")

if __name__ == '__main__':
    unittest.main()
