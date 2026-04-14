import allure
import pytest
from utils.datagenerator import DataGenerator
from data.project_data import InvalidProjectData
from utils.helpers import LIST_ID


@allure.feature("API. Tasks")
@allure.description("Создание таска через API")
def test_create_task(api_manager):
    with allure.step("Генерируем случайное имя задачи"):
        task_name = DataGenerator.fake_name()
        allure.attach(task_name, "Имя задачи", allure.attachment_type.TEXT)

    with allure.step("Отправляем POST-запрос на создание задачи"):
        response = api_manager.tasks.create_task(LIST_ID, data={"name": task_name})

    with allure.step("Проверяем статус-код 200"):
        with pytest.assume:
            assert response.status_code == 200
        data = response.json()

    with allure.step("Проверяем, что имя задачи совпадает"):
        with pytest.assume:
            assert data["name"] == task_name

    with allure.step(f"Удаляем задачу {data['id']}"):
        api_manager.tasks.delete_task(data["id"], expected_status=204)


@allure.feature("API. Tasks")
@allure.description("Получение таска по ID")
def test_get_task(created_task, api_manager):
    task_id = created_task
    allure.attach(str(task_id), "ID задачи", allure.attachment_type.TEXT)

    with allure.step(f"Отправляем GET-запрос для задачи {task_id}"):
        response = api_manager.tasks.get_task(task_id)

    with allure.step("Проверяем статус-код 200"):
        with pytest.assume:
            assert response.status_code == 200

    with allure.step("Проверяем, что ID в ответе совпадает с запрошенным"):
        with pytest.assume:
            assert response.json()["id"] == task_id


@allure.feature("API. Tasks")
@allure.description("Обновление таска")
def test_update_task(created_task, api_manager):
    task_id = created_task
    new_name = DataGenerator.fake_name()
    allure.attach(str(task_id), "ID задачи", allure.attachment_type.TEXT)
    allure.attach(new_name, "Новое имя", allure.attachment_type.TEXT)

    with allure.step(f"Отправляем PUT-запрос для задачи {task_id} с новым именем"):
        response = api_manager.tasks.update_task(task_id, name=new_name)

    with allure.step("Проверяем статус-код 200"):
        with pytest.assume:
            assert response.status_code == 200

    with allure.step("Проверяем, что имя в ответе обновлено"):
        with pytest.assume:
            assert response.json()["name"] == new_name


@allure.feature("API. Tasks")
@allure.description("Удаление таска")
def test_delete_task(api_manager):
    with allure.step("Генерируем случайное имя задачи"):
        task_name = DataGenerator.fake_name()
        allure.attach(task_name, "Имя задачи", allure.attachment_type.TEXT)

    with allure.step("Создаём задачу через API"):
        create_resp = api_manager.tasks.create_task(LIST_ID, data={"name": task_name})

    with allure.step("Проверяем успешность создания"):
        with pytest.assume:
            assert create_resp.status_code == 200
        task_id = create_resp.json()["id"]
        allure.attach(str(task_id), "ID задачи", allure.attachment_type.TEXT)

    with allure.step(f"Отправляем DELETE-запрос для задачи {task_id}"):
        delete_resp = api_manager.tasks.delete_task(task_id)

    with allure.step("Проверяем статус-код 204 (успешное удаление)"):
        with pytest.assume:
            assert delete_resp.status_code == 204


@allure.feature("API. Tasks Negative")
@allure.description("Создание таска с невалидными данными (параметризовано)")
@pytest.mark.parametrize("invalid_data", InvalidProjectData.invalid_task_data())
def test_create_task_negative(api_manager, invalid_data):
    allure.attach(str(invalid_data), "Невалидные данные", allure.attachment_type.JSON)

    with allure.step(
        "Отправляем POST-запрос с невалидными данными, ожидаем статус 400"
    ):
        response = api_manager.tasks.create_task(
            LIST_ID, data=invalid_data, expected_status=400
        )

    with allure.step("Проверяем, что статус-код равен 400"):
        with pytest.assume:
            assert response.status_code == 400


@allure.feature("API. Tasks Negative")
@allure.description("Получение несуществующего таска")
def test_get_nonexistent_task(api_manager):
    task_id = "000"
    allure.attach(task_id, "Несуществующий ID", allure.attachment_type.TEXT)

    with allure.step(
        f"Отправляем GET-запрос для несуществующей задачи {task_id}, ожидаем 401"
    ):
        response = api_manager.tasks.get_task(task_id, expected_status=401)

    with allure.step("Проверяем статус-код 401"):
        with pytest.assume:
            assert response.status_code == 401


@allure.feature("API. Tasks Negative")
@allure.description("Обновление несуществующего таска")
def test_update_nonexistent_task(api_manager):
    task_id = "000"
    allure.attach(task_id, "Несуществующий ID", allure.attachment_type.TEXT)

    with allure.step(
        f"Отправляем PUT-запрос для несуществующей задачи {task_id}, ожидаем 401"
    ):
        response = api_manager.tasks.update_task(task_id, expected_status=401)

    with allure.step("Проверяем статус-код 401"):
        with pytest.assume:
            assert response.status_code == 401


@allure.feature("API. Tasks Negative")
@allure.description("Удаление несуществующего таска")
def test_delete_nonexistent_task(api_manager):
    task_id = "000"
    allure.attach(task_id, "Несуществующий ID", allure.attachment_type.TEXT)

    with allure.step(
        f"Отправляем DELETE-запрос для несуществующей задачи {task_id}, ожидаем 401"
    ):
        response = api_manager.tasks.delete_task(task_id, expected_status=401)

    with allure.step("Проверяем статус-код 401"):
        with pytest.assume:
            assert response.status_code == 401
