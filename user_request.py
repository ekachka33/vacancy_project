from typing import List, Dict, Any, Callable
import json

from HH import HH


class UserAsk:
    """
    Класс для работы с запросами пользователя и управления вакансиями.
    Обеспечивает функционал добавления, поиска и удаления вакансий.
    """

    def __init__(self, file_name: str):
        """
        Инициализация класса UserAsk.

        Args:
            file_name (str): Имя файла для хранения вакансий
        """
        self.file_name = file_name

    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """
        Добавляет новую вакансию в файл.

        Args:
            vacancy (Dict[str, Any]): Словарь с данными вакансии
        """
        try:
            with open(self.file_name, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        except json.JSONDecodeError:
            data = []

        vacancy_dict = {
            "id": vacancy["id"],
            "name": vacancy["name"],
            "url": vacancy["url"],
            "salary": vacancy["salary"],
            "requirement": vacancy["description"],
        }

        # Проверяем на дубликаты
        if not any(v["id"] == vacancy_dict["id"] for v in data):
            data.append(vacancy_dict)

            with open(self.file_name, "w") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

    def get_vacancies(self, criteria: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        """
        Получает вакансии, соответствующие заданным критериям.

        Args:
            criteria (Callable[[Dict[str, Any]], bool]): Функция-критерий для фильтрации вакансий

        Returns:
            List[Dict[str, Any]]: Список отфильтрованных вакансий
        """
        try:
            with open(self.file_name, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        return [vacancy for vacancy in data if criteria(vacancy)]

    def delete_vacancy(self, vacancy_id: str) -> bool:
        """
        Удаляет вакансию по её ID.

        Args:
            vacancy_id (str): ID вакансии для удаления

        Returns:
            bool: True если вакансия была удалена, False если не найдена
        """
        try:
            with open(self.file_name, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

        initial_length = len(data)
        updated_data = [vacancy for vacancy in data if vacancy.get("id") != vacancy_id]

        if len(updated_data) < initial_length:
            with open(self.file_name, "w") as file:
                json.dump(updated_data, file, indent=4, ensure_ascii=False)
            return True
        return False

    def search_vac(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Поиск вакансий по ключевому слову в названии или описании.

        Args:
            keyword (str): Ключевое слово для поиска

        Returns:
            List[Dict[str, Any]]: Список найденных вакансий
        """
        return self.get_vacancies(
            lambda vacancy: keyword.lower() in vacancy["name"].lower() or
                            keyword.lower() in vacancy.get("requirement", "").lower()
        )

    def top_salary(self, n: int) -> List[Dict[str, Any]]:
        """
        Возвращает топ N вакансий по зарплате.

        Args:
            n (int): Количество вакансий для возврата

        Returns:
            List[Dict[str, Any]]: Список вакансий, отсортированных по зарплате
        """
        data = self.get_vacancies(lambda x: True)
        data.sort(key=lambda x: x["salary"] if x["salary"] is not None else 0, reverse=True)
        return data[:n]

    def fetch_vacancies_from_hh(self, keyword: str, pages: int = 1) -> List[Dict[str, Any]]:
        """
        Получает вакансии с HH.ru и сохраняет их в файл.

        Args:
            keyword (str): Ключевое слово для поиска
            pages (int): Количество страниц для загрузки

        Returns:
            List[Dict[str, Any]]: Список загруженных вакансий
        """
        hh = HH(self)
        return hh.load_vacancies(keyword, pages)
