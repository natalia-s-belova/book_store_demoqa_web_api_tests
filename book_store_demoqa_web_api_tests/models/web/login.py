from selene import browser, be, have, command
from book_store_demoqa_web_api_tests.data.users import User
import allure


class LoginPage:

    def __init__(self):
        self.user_name = browser.element('#userName')
        self.password = browser.element('#password')

    def open(self):
        with allure.step('Open Login page'):
            browser.open('/login')
            browser.all('[id^=google_ads][id$=container__]').with_(timeout=10).wait_until(
                have.size_greater_than_or_equal(3)
            )
            browser.all('[id^=google_ads][id$=container__]').perform(command.js.remove)

    def fill_user_name(self, value):
        with allure.step(f'Enter name "{value}"'):
            self.user_name.type(value)

    def fill_password(self, value):
        with allure.step(f'Enter password "{value}"'):
            self.password.type(value)

    def click_login(self):
        with allure.step('Click Login button'):
            browser.element('#login').click()

    def click_new_user(self):
        with allure.step('Click New User button'):
            browser.element('#newUser').click()

    def should_profile_be_opened(self):
        with allure.step('Verify Profile is opened'):
            browser.should(have.url('https://demoqa.com/profile'))

    def should_correct_username_be_shown(self, user: User):
        with allure.step(f'Verify username on the page is "{user.username}"'):
            browser.element('#userName-value').should(have.exact_text(user.username))

    def should_login_be_opened(self):
        with allure.step('Verify Login is opened'):
            browser.should(have.url('https://demoqa.com/login'))

    def should_register_be_opened(self):
        with allure.step('Verify Registration is opened'):
            browser.should(have.url('https://demoqa.com/register'))

    def should_error_be_shown(self):
        with allure.step('Verify error message is shown'):
            browser.element('#output #name').should(have.exact_text('Invalid username or password!'))

    def should_missing_field_be_highlighted(self, field):
        with allure.step('Verify missing field is highlighted in red'):
            field.should(have.css_property('border-color').value('rgb(220, 53, 69)'))

    def should_already_logged_in_be_shown(self):
        with allure.step('Verify logged in message is shown'):
            browser.element('#loading-label').should(have.text('You are already logged in.'))

    def open_login_in_left_panel(self):
        with allure.step('Click Login on the Left Panel'):
            browser.all('.menu-list .text').element_by(have.exact_text('Login')).click()
