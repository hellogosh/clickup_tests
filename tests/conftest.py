import sys
import os
import allure
from enums.browser import BROWSERS
from utils.browser_setup import BrowserSetup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from api.api_manager import ApiManager
from utils.datagenerator import DataGenerator
from utils.helpers import LIST_ID


import requests
from utils.helpers import CLICKUP_API_KEY, CLICKUP_EMAIL, CLICKUP_PASSWORD


@pytest.fixture(params=BROWSERS)
def browser(request):
    with allure.step(f"Запуск браузера {request.param}"):
        playwright, browser, context, page = BrowserSetup.setup(
            browser_type=request.param
        )
    yield page
    with allure.step("Закрытие браузера"):
        BrowserSetup.teardown(context, browser, playwright)


@pytest.fixture
def session():
    with allure.step("Создание HTTP-сессии с API-ключом"):
        http_session = requests.Session()
        http_session.headers.update({"Authorization": CLICKUP_API_KEY})
    yield http_session
    with allure.step("Закрытие HTTP-сессии"):
        http_session.close()


@pytest.fixture
def api_manager(session):
    with allure.step("Инициализация ApiManager"):
        return ApiManager(session)


@pytest.fixture
def created_task(api_manager):
    with allure.step("Создание задачи через API для теста"):
        task_name = DataGenerator.fake_name()
        response = api_manager.tasks.create_task(LIST_ID, data={"name": task_name})
        assert response.status_code == 200
        task_id = response.json()["id"]
        allure.attach(str(task_id), "Task ID", allure.attachment_type.TEXT)
    yield task_id
    with allure.step(f"Удаление задачи {task_id} после теста"):
        api_manager.tasks.delete_task(task_id, expected_status=204)


@pytest.fixture
def logged_in_page(browser):
    page = browser
    with allure.step("Переход на страницу логина ClickUp"):
        page.goto("https://app.clickup.com/login")
    with allure.step("Ожидание загрузки поля email"):
        page.wait_for_selector("#login-email-input", timeout=30000)
    with allure.step("Ввод email"):
        page.fill("#login-email-input", CLICKUP_EMAIL)
    with allure.step("Ввод пароля"):
        page.fill("#password-input", CLICKUP_PASSWORD)
    with allure.step("Нажатие кнопки Login"):
        page.wait_for_selector(
            '[data-test="login-submit"]:not([disabled])', timeout=5000
        )
        page.click('[data-test="login-submit"]')
    with allure.step("Ожидание перехода на дашборд"):
        page.wait_for_url("**/app.clickup.com/**", timeout=30000)
    with allure.step("Закрытие окна с куки (если появилось)"):
        accept_cookie = page.locator("button:has-text('Accept all')")
        if accept_cookie.is_visible():
            accept_cookie.click()
    return page


@pytest.fixture
def ui_task(api_manager):
    with allure.step("Создание задачи через API для UI-теста"):
        task_name = DataGenerator.fake_name()
        response = api_manager.tasks.create_task(
            LIST_ID, data={"name": task_name}, expected_status=200
        )
        task_id = response.json()["id"]
        allure.attach(str(task_id), "Task ID", allure.attachment_type.TEXT)
        allure.attach(task_name, "Task Name", allure.attachment_type.TEXT)
    yield {"id": task_id, "name": task_name}
    with allure.step(f"Удаление задачи {task_id} после UI-теста"):
        api_manager.tasks.delete_task(task_id, expected_status=204)
