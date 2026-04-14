from api.tasks_api import TasksAPI


class ApiManager:
    def __init__(self, session):
        self.session = session
        self.tasks = TasksAPI(session)
