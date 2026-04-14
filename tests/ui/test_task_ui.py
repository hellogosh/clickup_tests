import allure
from utils.helpers import TEAM_ID, LIST_ID


@allure.feature("UI. Управление задачами")
@allure.description("Удаление задачи через UI")
def test_delete_task_via_ui(api_manager, logged_in_page, ui_task):
    task = ui_task
    task_id = task["id"]
    task_name = task["name"]

    allure.attach(str(task_id), "Task ID", allure.attachment_type.TEXT)
    allure.attach(task_name, "Task Name", allure.attachment_type.TEXT)

    # 1. Переход на доску и проверка видимости задачи
    with allure.step("Переход на доску задач"):
        board_url = f"https://app.clickup.com/{TEAM_ID}/v/l/li/{LIST_ID}"
        logged_in_page.goto(board_url)
        logged_in_page.wait_for_selector(
            "[data-test='task-row-main__link']", timeout=10000
        )

    with allure.step(f"Проверка, что задача '{task_name}' отображается на доске"):
        assert logged_in_page.locator(f"text='{task_name}'").first.is_visible(), (
            f'Задача "{task_name}" не отображается на доске'
        )

    # 2. Открытие задачи напрямую по ID
    with allure.step(
        f"Открытие задачи по прямому URL: https://app.clickup.com/t/{task_id}"
    ):
        task_url = f"https://app.clickup.com/t/{task_id}"
        logged_in_page.goto(task_url)

    # 3. Поиск и нажатие кнопки меню (три точки)
    with allure.step("Поиск кнопки меню (три точки) в правом верхнем углу"):
        menu_button = logged_in_page.locator(
            '[data-test="task-view-header__task-settings"]'
        )
        menu_button.click()

    # 4. Нажатие кнопки Delete в выпадающем меню
    with allure.step("Нажатие кнопки Delete в выпадающем меню"):
        delete_btn = logged_in_page.locator(
            '[data-test="dropdown-list-item__cu-task-view-menu-delete"]'
        )
        delete_btn.click()

    # 5. Проверка, что задача удалена (перенаправление на доску и отсутствие текста задачи)
    with allure.step("Ожидание перенаправления на доску задач"):
        logged_in_page.wait_for_url(f"**/v/l/li/{LIST_ID}", timeout=10000)

    with allure.step(
        f"Проверка, что задача '{task_name}' больше не отображается на доске"
    ):
        logged_in_page.wait_for_selector(
            f"text='{task_name}'", state="hidden", timeout=5000
        )

    # 6. Дополнительная проверка через API
    with allure.step("Проверка удаления задачи через API (ожидаем статус 404)"):
        get_resp = api_manager.tasks.get_task(task_id, expected_status=404)
        assert get_resp.status_code == 404, (
            f"Ожидался статус 404, получен {get_resp.status_code}"
        )
