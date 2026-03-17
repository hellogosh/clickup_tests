import pytest
from utils.datagenerator import DataGenerator
from data.project_data import InvalidProjectData

LIST_ID = "901521528654"

def test_create_task(api_manager):
    task_name = DataGenerator.fake_name()
    response = api_manager.tasks.create_task(LIST_ID, data={"name": task_name})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == task_name
    api_manager.tasks.delete_task(data["id"], expected_status=204)

def test_get_task(created_task, api_manager):
    task_id = created_task
    response = api_manager.tasks.get_task(task_id)
    assert response.status_code == 200
    assert response.json()["id"] == task_id

def test_update_task(created_task, api_manager):
    new_name = DataGenerator.fake_name()
    response = api_manager.tasks.update_task(created_task, name=new_name)
    assert response.status_code == 200
    assert response.json()["name"] == new_name

def test_delete_task(api_manager):
    task_name = DataGenerator.fake_name()
    create_resp = api_manager.tasks.create_task(LIST_ID, data={"name": task_name})
    assert create_resp.status_code == 200
    task_id = create_resp.json()["id"]
    delete_resp = api_manager.tasks.delete_task(task_id)
    assert delete_resp.status_code == 204

@pytest.mark.parametrize("invalid_data", InvalidProjectData.invalid_task_data())
def test_create_task_negative(api_manager, invalid_data):
    response = api_manager.tasks.create_task(LIST_ID, data=invalid_data, expected_status=400)
    assert response.status_code == 400

def test_get_nonexistent_task(api_manager):
    task_id = '000'
    response = api_manager.tasks.get_task(task_id, expected_status=401)
    assert response.status_code == 401

def test_update_nonexistent_task(api_manager):
    task_id = '000'
    response = api_manager.tasks.update_task(task_id, expected_status=401)
    assert response.status_code == 401

def test_delete_nonexistent_task(api_manager):
    task_id = '000'
    response = api_manager.tasks.delete_task(task_id, expected_status=401)
    assert response.status_code == 401
