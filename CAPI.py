from abc import ABC, abstractmethod
from typing import Any, List, Dict, Callable


class Parser(ABC):
    """
    Абстрактный базовый класс для работы с API сервисов вакансий.
    Определяет основной интерфейс для работы с вакансиями.
    """

    @abstractmethod
    def add_vac(self, vacancy: Dict[str, Any]) -> None:
        """
        Абстрактный метод для добавления вакансии.

        Args:
            vacancy (Dict[str, Any]): Данные вакансии для добавления
        """
        pass

    @abstractmethod
    def get_vac(self, criteria: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        """
        Абстрактный метод для получения вакансий по критериям.

        Args:
            criteria (Callable[[Dict[str, Any]], bool]): Функция-критерий для фильтрации

        Returns:
            List[Dict[str, Any]]: Список отфильтрованных вакансий
        """
        pass

    @abstractmethod
    def del_vac(self, vacancy_id: str) -> bool:
        """
        Абстрактный метод для удаления вакансии.

        Args:
            vacancy_id (str): ID вакансии для удаления

        Returns:
            bool: Результат операции удаления
        """
        pass
