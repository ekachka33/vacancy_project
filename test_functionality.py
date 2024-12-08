from user_ask import UserAsk
from hh import HH

def main():
    # Инициализация
    user_ask = UserAsk("vacancies.json")
    hh = HH(user_ask)
    
    print("=== Тест поиска вакансий ===")
    # Поиск вакансий Python разработчика
    vacancies = hh.get_vacancies_by_keyword("Python Developer")
    print(f"Найдено вакансий: {len(vacancies)}")
    
    if vacancies:
        print("\n=== Пример первой вакансии ===")
        first_vacancy = vacancies[0]
        print(f"Название: {first_vacancy.get('name')}")
        print(f"URL: {first_vacancy.get('alternate_url')}")
        if first_vacancy.get('salary'):
            print(f"Зарплата: {first_vacancy['salary']}")
        
        # Сохранение вакансий
        print("\n=== Тест сохранения вакансий ===")
        hh.add_vac(first_vacancy)
        print("Вакансия сохранена")
        
        # Проверка чтения сохраненных вакансий
        print("\n=== Тест чтения вакансий ===")
        saved_vacancies = user_ask.get_vacancies(lambda v: True)
        print(f"Количество сохраненных вакансий: {len(saved_vacancies)}")
        
        # Проверка фильтрации
        print("\n=== Тест фильтрации вакансий ===")
        python_vacancies = user_ask.get_vacancies(lambda v: "Python" in v.get("name", ""))
        print(f"Найдено Python вакансий: {len(python_vacancies)}")

if __name__ == "__main__":
    main()
