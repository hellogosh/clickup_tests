from  custom_requester.customrequester import CustomRequester

class TasksAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session)

    def create_task(self, list_id, name, description=None):
        payload = {"name": name}
        if description:
            payload["description"] = description
        return self.send_request("POST", f"/list/{list_id}/task", data=payload, expected_status=200)

    def get_task(self, task_id):
        return self.send_request("GET", f"/task/{task_id}", expected_status=200)

    def update_task(self, task_id, **kwargs):
        return self.send_request("PUT", f"/task/{task_id}", data=kwargs, expected_status=200)

    def delete_task(self, task_id):
        return self.send_request("DELETE", f"/task/{task_id}", expected_status=204)