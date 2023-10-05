import allure
# from allure import step
from selene.support.shared import browser
from book_store_demoqa_web_api_tests.utils import api_helper
from book_store_demoqa_web_api_tests.data.users import User
from selene import have, command


def create_account_via_api(user: User):
    with allure.step('Via API: Create new user'):
        response = api_helper.post_user(user)
        user.userid = response.json()['userID']
        user.books = []
        return user


def login_via_api(user: User):
    generate_token_if_required(user)

    with allure.step("Add auth cookie to browser and refresh page"):
        browser.driver.add_cookie({"name": 'token', "value": user.token})
        browser.driver.add_cookie({"name": 'expires', "value": user.token_expires})
        browser.driver.add_cookie({"name": 'userName', "value": user.username})
        browser.driver.add_cookie({"name": 'userID', "value": user.userid})
        browser.driver.refresh()
        browser.all('[id^=google_ads][id$=container__]').with_(timeout=10).wait_until(
            have.size_greater_than_or_equal(3)
        )
        browser.all('[id^=google_ads][id$=container__]').perform(command.js.remove)


def add_books_for_user(isbns: list, user: User):
    with allure.step(f'Via API: Add books with isbns {isbns} for {user.username}'):
        generate_token_if_required(user)
        user.books = api_helper.add_books_for_user(isbns, user).json()['books']
        return user


def verify_books_list_via_api(user: User, books: list):
    with allure.step(f'Via API: Verify books {[book["title"] for book in books]} are added for {user.username}'):
        generate_token_if_required(user)
        response = api_helper.get_user(user)
        assert response.json()['books'] == books


def delete_acc_via_api(user: User):
    with allure.step('Via API: Delete user'):
        generate_token_if_required(user)
        api_helper.delete_user(user)


def generate_token_if_required(user: User):
    if user.token == '':
        with allure.step('Generation of token as it is not generated yet'):
            response = api_helper.generate_token(user)
            user.token = response.json()['token']
            user.token_expires = response.json()['expires']
