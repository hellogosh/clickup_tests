from  custom_requester.customrequester import CustomRequester

class TasksAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session)

    def create_task(self, list_id, data, expected_status=200):
        return self.send_request("POST", f"/list/{list_id}/task", data=data, expected_status=expected_status)

    def get_task(self, task_id, expected_status=200):
        return self.send_request("GET", f"/task/{task_id}", expected_status=expected_status)

    def update_task(self, task_id, expected_status=200, **kwargs):
        return self.send_request("PUT", f"/task/{task_id}", data=kwargs, expected_status=expected_status)

    def delete_task(self, task_id, expected_status=204):
        return self.send_request("DELETE", f"/task/{task_id}", expected_status=expected_status)