from dataclasses import dataclass
from typing import Optional
import uuid


@dataclass
class Sort_Vacan:
    """
    Класс для представления вакансии с поддержкой сравнения по зарплате.
    Использует dataclass для автоматической генерации методов сравнения.
    """

    name: str
    url: str
    salary: int
    description: str
    id: str = None

    def __post_init__(self):
        """
        Пост-инициализация для установки ID и валидации данных.
        """
        if self.id is None:
            self.id = str(uuid.uuid4())
        self._validate_data()

    def _validate_data(self) -> None:
        """
        Приватный метод для валидации данных вакансии.
        """
        if not isinstance(self.salary, (int, float)):
            self.salary = 0

        if not self.description:
            self.description = "Описание не указано"

        if not self.url:
            self.url = "#"

    def to_dict(self) -> dict:
        """
        Преобразует объект вакансии в словарь.

        Returns:
            dict: Словарь с данными вакансии
        """
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "salary": self.salary,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Sort_Vacan':
        """
        Создает объект вакансии из словаря.

        Args:
            data (dict): Словарь с данными вакансии

        Returns:
            Sort_Vacan: Новый объект вакансии
        """
        return cls(
            name=data["name"],
            url=data["url"],
            salary=data.get("salary", 0),
            description=data.get("description", ""),
            id=data.get("id")
        )
