

def test_authorization(browser):

    browser.goto('https://app.clickup.com/login')
    browser.wait_for_selector("#login-email-input")
    browser.fill('#login-email-input', 'georgypant@mail.ru')
    browser.fill('#password-input', '12135160Aa!')
    browser.click('[data-test="login-submit"]')
    browser.wait_for_url('https://app.clickup.com/90152324458/v/l/li/901521528654')


def test_invalid_password(browser):

    browser.goto('https://app.clickup.com/login')
    browser.wait_for_selector("#login-email-input")
    browser.fill('#login-email-input', 'georgypant@mail.ru')
    browser.fill('#password-input', '12135160Aa!oascjp')
    browser.click('[data-test="login-submit"]')

    error = browser.locator('.cu-password-input__error')
    error.wait_for(state="visible", timeout=5000)
    assert error.is_visible(), 'Сообщение об ошибке не появилось'
