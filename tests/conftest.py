import sys
import os
import time

from enums.browser import BROWSERS
from utils.browser_setup import BrowserSetup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from api.api_manager import ApiManager
from utils.datagenerator import DataGenerator

LIST_ID = "901521528654"

import requests
from utils.helpers import CLICKUP_API_KEY, CLICKUP_EMAIL, CLICKUP_PASSWORD
from enums.host import BASE_URL

@pytest.fixture(params=BROWSERS)
def browser(request):
    playwright, browser, context, page = BrowserSetup.setup(browser_type=request.param)
    yield page
    BrowserSetup.teardown(context, browser, playwright)


@pytest.fixture
def session():
    """Возвращает экземпляр API-клиента с настроенной сессией."""
    http_session = requests.Session()
    http_session.headers.update({"Authorization": CLICKUP_API_KEY})
    yield http_session
    http_session.close()

@pytest.fixture
def api_manager(session):
    """Возвращает ApiManager с настроенной сессией."""
    return ApiManager(session)

@pytest.fixture
def created_task(api_manager):
    """Создаёт задачу перед тестом и удаляет после."""
    task_name = DataGenerator.fake_name()
    response = api_manager.tasks.create_task(LIST_ID, data={"name": task_name})
    assert response.status_code == 200
    task_id = response.json()["id"]
    yield task_id
    api_manager.tasks.delete_task(task_id, expected_status=204)


@pytest.fixture
def logged_in_page(browser):
    """Фикстура возвращает авторизованную страницу."""
    page = browser
    page.goto("https://app.clickup.com/login")
    time.sleep(15)
    page.wait_for_selector("#login-email-input", timeout=10000)
    page.fill("#login-email-input", CLICKUP_EMAIL)
    page.fill("#password-input", CLICKUP_PASSWORD)

    page.wait_for_selector('[data-test="login-submit"]:not([disabled])', timeout=5000)
    page.click('[data-test="login-submit"]')
    time.sleep(10)
    page.wait_for_url("**/app.clickup.com/**", timeout=30000)

    accept_cookie = page.locator("button:has-text('Accept all')")
    if accept_cookie.is_visible():
        accept_cookie.click()
    return page

@pytest.fixture
def ui_task(api_manager):
    """Создаёт задачу через API для UI-тестов. Возвращает словарь {id, name}."""
    task_name = DataGenerator.fake_name()
    response = api_manager.tasks.create_task(LIST_ID, data={"name": task_name}, expected_status=200)
    task_id = response.json()["id"]
    yield {"id": task_id, "name": task_name}
    api_manager.tasks.delete_task(task_id, expected_status=204)


'90152324458/v/o/s/90159813129'

