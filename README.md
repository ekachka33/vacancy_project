# Vacancy Project

Проект для работы с вакансиями с сайта HeadHunter. Позволяет искать, сохранять и управлять вакансиями.

## Особенности

- Поиск вакансий по ключевым словам
- Добавление и удаление вакансий
- Валидация данных вакансий

## Требования

- Python 3.7+
- Установленные зависимости из requirements.txt

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ekachka33/vacancy_project.git
cd vacancy_project
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/macOS
# или
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Использование

```python
from HH import HH
from user_request import UserAsk

# Создаем объект для работы с файлами
user_ask = UserAsk("vacancies.json")

# Создаем объект для работы с API HH
hh = HH(user_ask)

# Ищем вакансии
vacancies = hh.get_vacancies_by_keyword("Python Developer")

# Сохраняем вакансии
for vacancy in vacancies:
    hh.add_vac(vacancy)

# Получаем сохраненные вакансии
python_vacancies = hh.get_vac(lambda v: "Python" in v["name"])
```

## Тестирование

Для запуска тестов используйте pytest:

```bash
pytest tests/
```

## Требования

- Python 3.7+
- requests>=2.31.0
- typing-extensions>=4.7.1
- pytest>=7.4.0 (для тестов)
- coverage>=7.3.0 (для проверки покрытия кода)
- black>=23.7.0 (для форматирования кода)
- flake8>=6.1.0 (для проверки стиля кода)
- mypy>=1.5.0 (для проверки типов)

## Лицензия

MIT License
