import pytest
from utils.helpers import TEAM_ID, LIST_ID

def test_delete_task_via_ui(api_manager, logged_in_page, ui_task):
    task = ui_task
    task_id = task["id"]
    task_name = task["name"]

    # 1. Переходим на доску и убеждаемся, что задача видна
    board_url = f"https://app.clickup.com/{TEAM_ID}/v/l/li/{LIST_ID}"
    logged_in_page.goto(board_url)
    logged_in_page.wait_for_selector("[data-test='task-row-main__link']", timeout=10000)
    assert logged_in_page.locator(f"text='{task_name}'").first.is_visible(), \
        f'Задача "{task_name}" не отображается на доске'

    #2. Открываем задачу напрямую по ID
    task_url = f"https://app.clickup.com/t/{task_id}"
    logged_in_page.goto(task_url)

    #3. Находим кнопку меню (три точки) в правом верхнем углу
    menu_button = logged_in_page.locator('[data-test="task-view-header__task-settings"]')
    menu_button.click()

    #4.В выпадающем меню нажимаем Delete
    delete_btn = logged_in_page.locator('[data-test="dropdown-list-item__cu-task-view-menu-delete"]')
    delete_btn.click()

    #5.Проверяем, что задача исчезла (перенаправление на доску или 404)
    logged_in_page.wait_for_url(f"**/v/l/li/{LIST_ID}", timeout=10000)
    logged_in_page.wait_for_selector(f"text='{task_name}'", state="hidden", timeout=5000)

    #6. Дополнительная проверка через API
    get_resp = api_manager.tasks.get_task(task_id, expected_status=404)
    assert get_resp.status_code == 404