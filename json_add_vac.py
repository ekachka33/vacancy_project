import json


class JSONVacancy:
    def __init__(self, file_name):
        self.file_name = file_name

    def add_vacancy(self, vacancy):
        try:
            with open(self.file_name, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        vacancy_dict = {
            "id": vacancy["id"],
            "name": vacancy["name"],
            "url": vacancy["url"],
            "salary": vacancy["salary"],
            "description": vacancy["description"],
        }
        data.append(vacancy_dict)

        with open(self.file_name, "w") as file:
            json.dump(data, file, indent=4)

    def get_vacancies(self, criteria):
        try:
            with open(self.file_name, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return []

        return [vacancy for vacancy in data if criteria(vacancy)]

    def delete_vacancy(self, vacancy_id):
        try:
            with open(self.file_name, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return

        updated_data = [vacancy for vacancy in data if vacancy.get("id") != vacancy_id]

        with open(self.file_name, "w") as file:
            json.dump(updated_data, file, indent=4)
