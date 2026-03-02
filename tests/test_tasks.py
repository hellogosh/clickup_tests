import pytest
from utils.datagenerator import DataGenerator


LIST_ID = "901521528654"

def test_create_task(api_manager):
    task_name = DataGenerator.fake_name()
    response = api_manager.tasks.create_task(LIST_ID, task_name)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == task_name
    # Очистка вручную (или можно через фикстуру, но здесь проще сразу удалить)
    api_manager.tasks.delete_task(data["id"])

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
    create_resp = api_manager.tasks.create_task(LIST_ID, task_name)
    assert create_resp.status_code == 200
    task_id = create_resp.json()["id"]
    delete_resp = api_manager.tasks.delete_task(task_id)
    assert delete_resp.status_code == 204

    # Проверяем, что задача действительно удалена
    with pytest.raises(ValueError) as exc_info:
        api_manager.tasks.get_task(task_id)
    assert "404" in str(exc_info.value)