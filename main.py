from typing import Optional, List, Dict, Any
from user_request import UserAsk
from CV import Sort_Vacan


def print_vacancy(vacancy: Dict[str, Any]) -> None:
    """
    Выводит информацию о вакансии в читаемом формате.

    Args:
        vacancy (Dict[str, Any]): Данные вакансии
    """
    print("\n" + "=" * 50)
    print(f"Название: {vacancy['name']}")
    print(f"URL: {vacancy['url']}")
    print(f"Зарплата: {vacancy['salary'] if vacancy['salary'] else 'Не указана'}")
    print(f"Описание: {vacancy['requirement']}")
    print("=" * 50)


def main():
    """
    Основная функция программы, обеспечивающая взаимодействие с пользователем.
    """
    file_name = "new_vacancies.json"
    user_ask = UserAsk(file_name)

    while True:
        print("\nМенеджер вакансий HH.ru")
        print("1. Добавить вакансию")
        print("2. Найти вакансии по ключевому слову")
        print("3. Получить топ N вакансий по зарплате")
        print("4. Удалить вакансию")
        print("5. Загрузить вакансии из hh.ru")
        print("6. Выход")

        try:
            choice = input("\nВыберите действие: ")

            if choice == "1":
                try:
                    name = input("Введите название вакансии: ")
                    url = input("Введите URL вакансии: ")
                    salary = int(input("Введите зарплату (0 если не указана): "))
                    description = input("Введите описание вакансии: ")
                    vacancy_id = input("Введите уникальный ID вакансии: ")

                    vacancy = {
                        "id": vacancy_id,
                        "name": name,
                        "url": url,
                        "salary": salary,
                        "description": description,
                    }
                    user_ask.add_vacancy(vacancy)
                    print("Вакансия успешно добавлена!")
                except ValueError as e:
                    print(f"Ошибка при добавлении вакансии: {e}")

            elif choice == '2':
                keyword = input("Введите ключевое слово для поиска: ")
                results = user_ask.search_vac(keyword)
                if results:
                    print("\nНайденные вакансии:")
                    for vac in results:
                        print_vacancy(vac)
                else:
                    print("Вакансии не найдены.")

            elif choice == "3":
                try:
                    n = int(input("Сколько вакансий показать? "))
                    if n <= 0:
                        raise ValueError("Количество вакансий должно быть положительным числом")

                    top_vacancies = user_ask.top_salary(n)
                    if top_vacancies:
                        print("\nТоп вакансий по зарплате:")
                        for vac in top_vacancies:
                            print_vacancy(vac)
                    else:
                        print("Вакансии не найдены.")
                except ValueError as e:
                    print(f"Ошибка: {e}")

            elif choice == "4":
                vacancy_id = input("Введите ID вакансии для удаления: ")
                if user_ask.delete_vacancy(vacancy_id):
                    print("Вакансия успешно удалена!")
                else:
                    print("Вакансия не найдена.")

            elif choice == "5":
                try:
                    keyword = input("Введите ключевое слово для поиска вакансий: ")
                    pages = int(input("Сколько страниц загрузить (по 20 вакансий на странице): "))
                    if pages <= 0:
                        raise ValueError("Количество страниц должно быть положительным числом")

                    vacancies = user_ask.fetch_vacancies_from_hh(keyword, pages)
                    print(f"Загружено {len(vacancies)} вакансий.")
                except ValueError as e:
                    print(f"Ошибка: {e}")
                except Exception as e:
                    print(f"Произошла ошибка при загрузке вакансий: {e}")

            elif choice == "6":
                print("Выход из программы.")
                break

            else:
                print("Неверный выбор. Попробуйте снова.")

        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()

