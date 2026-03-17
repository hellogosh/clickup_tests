from utils.datagenerator import DataGenerator

class InvalidProjectData:
    @staticmethod
    def invalid_task_data():
        return [
            {'name': ''},
            {},
            {"name": None}
        ]