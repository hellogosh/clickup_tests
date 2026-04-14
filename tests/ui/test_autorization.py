import allure


@allure.feature("UI. Авторизация")
@allure.story("Успешная авторизация")
@allure.title("Проверка успешной авторизации")
@allure.description(
    "Тест проверяет возможность входа в аккаунт с валидными учетными данными"
)
def test_authorization(browser):
    with allure.step("Переход на страницу логина ClickUp"):
        browser.goto("https://app.clickup.com/login")
        browser.wait_for_selector("#login-email-input", timeout=10000)

    with allure.step("Ввод email"):
        browser.fill("#login-email-input", "georgypant@mail.ru")

    with allure.step("Ввод пароля"):
        browser.fill("#password-input", "12135160Aa!")

    with allure.step("Нажатие кнопки 'Log In'"):
        browser.click('[data-test="login-submit"]')

    with allure.step("Ожидание перехода на дашборд"):
        browser.wait_for_url(
            "https://app.clickup.com/90152324458/v/l/li/901521528654", timeout=30000
        )

    with allure.step(
        "Проверка, что элемент профиля отображается (авторизация успешна)"
    ):
        browser.wait_for_selector('[data-test="user-menu-trigger"]', timeout=10000)
        assert browser.locator('[data-test="user-menu-trigger"]').is_visible()


@allure.feature("UI. Авторизация")
@allure.story("Неудачная авторизация")
@allure.title("Проверка ошибки при неверном пароле")
@allure.description(
    "Тест проверяет, что при вводе неверного пароля появляется сообщение об ошибке"
)
def test_invalid_password(browser):
    with allure.step("Переход на страницу логина ClickUp"):
        browser.goto("https://app.clickup.com/login")
        browser.wait_for_selector("#login-email-input", timeout=10000)

    with allure.step("Ввод email"):
        browser.fill("#login-email-input", "georgypant@mail.ru")

    with allure.step("Ввод неверного пароля"):
        browser.fill("#password-input", "12135160Aa!oascjp")

    with allure.step("Нажатие кнопки 'Log In'"):
        browser.click('[data-test="login-submit"]')

    with allure.step("Ожидание появления сообщения об ошибке"):
        error = browser.locator(".cu-password-input__error")
        error.wait_for(state="visible", timeout=5000)

    with allure.step("Проверка, что сообщение об ошибке отображается"):
        assert error.is_visible(), "Сообщение об ошибке не появилось"
