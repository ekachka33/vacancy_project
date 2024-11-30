from typing import List, Dict, Any
import requests
from CAPI import Parser


class HH(Parser):
    """
    Класс для работы с API HeadHunter.
    Наследуется от абстрактного класса Parser.
    """

    def __init__(self, file_worker: Any):
        """
        Инициализация класса HH.

        Args:
            file_worker: Объект для работы с файлами
        """
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.file_worker = file_worker

    def add_vac(self, vacancy: Dict[str, Any]) -> None:
        """
        Добавляет вакансию в хранилище.

        Args:
            vacancy (Dict[str, Any]): Данные вакансии
        """
        self.file_worker.add_vacancy(vacancy)

    def get_vac(self, criteria: Any) -> List[Dict[str, Any]]:
        """
        Получает вакансии по заданным критериям.

        Args:
            criteria: Критерии поиска вакансий

        Returns:
            List[Dict[str, Any]]: Список найденных вакансий
        """
        return self.file_worker.get_vacancies(criteria)

    def del_vac(self, vacancy_id: str) -> bool:
        """
        Удаляет вакансию по ID.

        Args:
            vacancy_id (str): ID вакансии

        Returns:
            bool: Результат удаления
        """
        return self.file_worker.delete_vacancy(vacancy_id)

    def load_vacancies(self, keyword: str, pages: int = 1) -> List[Dict[str, Any]]:
        """
        Загружает вакансии с HH.ru по ключевому слову.

        Args:
            keyword (str): Ключевое слово для поиска
            pages (int): Количество страниц для загрузки

        Returns:
            List[Dict[str, Any]]: Список загруженных вакансий
        """
        self.params['text'] = keyword
        loaded_vacancies = []

        try:
            for page in range(min(pages, 20)):  # Ограничиваем максимум 20 страницами
                self.params['page'] = page
                response = requests.get(self.url, headers=self.headers, params=self.params)
                response.raise_for_status()

                data = response.json()
                vacancies = data.get('items', [])

                for vac in vacancies:
                    vacancy = {
                        "id": vac["id"],
                        "name": vac["name"],
                        "url": vac["alternate_url"],  # Используем alternate_url для прямой ссылки
                        "salary": self._parse_salary(vac.get("salary")),
                        "description": vac.get("snippet", {}).get("requirement", "Описание не указано"),
                    }
                    self.add_vac(vacancy)
                    loaded_vacancies.append(vacancy)

        except requests.RequestException as e:
            print(f"Ошибка при загрузке вакансий: {e}")
            return loaded_vacancies

        return loaded_vacancies

    def _parse_salary(self, salary_data: Dict[str, Any]) -> int:
        """
        Парсит данные о зарплате из ответа API.

        Args:
            salary_data (Dict[str, Any]): Данные о зарплате

        Returns:
            int: Значение зарплаты или 0, если зарплата не указана
        """
        if not salary_data:
            return 0

        # Берем минимальную зарплату, если указана
        salary = salary_data.get('from', 0)
        if not salary:
            # Если минимум не указан, берем максимум
            salary = salary_data.get('to', 0)

        return salary or 0  # Возвращаем 0, если зарплата None
