import string
from faker import Faker

faker_instance = Faker()

class DataGenerator:
    @staticmethod
    def fake_project():
        first_letter = faker_instance.random.choice(string.ascii_letters)
        rest_charachters = ''.join(faker_instance.random.choices(string.ascii_letters + string.digits, k = 10))
        project_id = first_letter + rest_charachters
        return project_id


    @staticmethod
    def fake_name():
        return faker_instance.word()
