from book_store_demoqa_web_api_tests.data.users import User
from book_store_demoqa_web_api_tests.models.web.login import LoginPage
import allure
from allure_commons.types import Severity

pytestmark = [
    allure.label('layer', 'UI test'),
    allure.label('owner', 'natalia_belova'),
    allure.epic('BookStore Web'),
    allure.tag('web'),
    allure.feature('Login')
]

user = User(username='nikola_jokic', password='Test1234!', userid='8d694a81-eb06-41be-ad46-1bed792d2ffc', books=[])


@allure.title("Verify successful login")
@allure.severity(Severity.BLOCKER)
def test_successful_login():
    # GIVEN
    login_page = LoginPage()
    login_page.open()

    # WHEN
    login_page.fill_user_name(user.username)
    login_page.fill_password(user.password)
    login_page.click_login()

    # THEN
    login_page.should_profile_be_opened()
    login_page.should_correct_username_be_shown(user)


@allure.title("Verify unsuccessful login due to missing password")
@allure.severity(Severity.CRITICAL)
def test_unsuccessful_login_missing_password():
    # GIVEN
    login_page = LoginPage()
    login_page.open()

    # WHEN
    login_page.fill_user_name(user.username)
    login_page.click_login()

    # THEN
    login_page.should_login_be_opened()
    login_page.should_missing_field_be_highlighted(login_page.password)


@allure.title("Verify unsuccessful login due to missing username")
@allure.severity(Severity.CRITICAL)
def test_unsuccessful_login_missing_username():
    # GIVEN
    login_page = LoginPage()
    login_page.open()

    # WHEN
    login_page.fill_password(user.password)
    login_page.click_login()

    # THEN
    login_page.should_login_be_opened()
    login_page.should_missing_field_be_highlighted(login_page.user_name)


@allure.title("Verify unsuccessful login due to invalid password")
@allure.severity(Severity.BLOCKER)
def test_unsuccessful_login_invalid_password():
    # GIVEN
    login_page = LoginPage()
    login_page.open()

    # WHEN
    login_page.fill_user_name(user.username)
    login_page.fill_password('invalid_value')
    login_page.click_login()

    # THEN
    login_page.should_login_be_opened()
    login_page.should_error_be_shown()


@allure.title("Verify unsuccessful login due to non-existing account used")
@allure.severity(Severity.NORMAL)
def test_unsuccessful_login_non_existing_user():
    # GIVEN
    login_page = LoginPage()
    login_page.open()

    # WHEN
    login_page.fill_user_name(user.username + '_invalid_addition')
    login_page.fill_password(user.password)
    login_page.click_login()

    # THEN
    login_page.should_login_be_opened()
    login_page.should_error_be_shown()


@allure.title("Verify going from Login to Registration")
@allure.severity(Severity.NORMAL)
def test_registration_page_opening():
    # GIVEN
    login_page = LoginPage()
    login_page.open()

    # WHEN
    login_page.click_new_user()

    # THEN
    login_page.should_register_be_opened()


@allure.title("Verify Already Logged In message")
@allure.severity(Severity.NORMAL)
def test_already_logged_in():
    # GIVEN
    login_page = LoginPage()
    login_page.open()

    # WHEN
    login_page.fill_user_name(user.username)
    login_page.fill_password(user.password)
    login_page.click_login()
    login_page.open_login_in_left_panel()

    # THEN
    login_page.should_already_logged_in_be_shown()
    login_page.should_correct_username_be_shown(user)
