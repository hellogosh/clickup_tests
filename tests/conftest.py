import sys
import os

from enums.browser import BROWSERS
from utils.browser_setup import BrowserSetup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from api.api_manager import ApiManager
from utils.datagenerator import DataGenerator

LIST_ID = "901521528654"

import requests
from utils.helpers import CLICKUP_API_KEY
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

