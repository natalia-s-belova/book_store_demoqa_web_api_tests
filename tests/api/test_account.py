from book_store_demoqa_web_api_tests.utils import api_helper
from book_store_demoqa_web_api_tests.models.api import book_store_api
from book_store_demoqa_web_api_tests.data.users import User
import allure
from allure_commons.types import Severity

user1 = User(username='lebron_james', password='Test123!')

user2 = User(username='nikola_jokic', password='Test1234!', userid='8d694a81-eb06-41be-ad46-1bed792d2ffc', books=[])

user3 = User(username='michael_jordan', password='Test1234!', userid='60e853c9-c3da-493c-8cde-b9526a243c64', books=[{
    "isbn": "9781449325862",
    "title": "Git Pocket Guide",
    "subTitle": "A Working Introduction",
    "author": "Richard E. Silverman",
    "publish_date": "2020-06-04T08:48:39.000Z",
    "publisher": "O'Reilly Media",
    "pages": 234,
    "description": "This pocket guide is the perfect on-the-job companion to Git, the distributed version control system. It provides a compact, readable introduction to Git for new users, as well as a reference to common commands and procedures for those of you with Git exp",
    "website": "http://chimera.labs.oreilly.com/books/1230000000561/index.html"}])

user4 = User(username='ivan_edeshko', password='Test1234!', userid='4ec0f63e-4956-4cb1-b284-cd81d467a308', books=[])


pytestmark = [
    allure.label('layer', 'API test'),
    allure.label('owner', 'natalia_belova'),
    allure.epic('BookStore API'),
    allure.tag('REST'),
    allure.feature('Account')
]


@allure.title('Verify successful  creation and deletion if a user')
@allure.severity(Severity.BLOCKER)
def test_create_then_delete_user():
    # WHEN
    response1 = api_helper.post_user(user1)

    # THEN
    book_store_api.verify_code(response1, 201)
    book_store_api.verify_response_json(response1, 'username', user1.username)
    book_store_api.verify_response_json(response1, 'books', [])
    book_store_api.verify_schema(response1, 'post_account.json')

    # GIVEN
    user1.userid = response1.json()['userID']
    response2 = api_helper.generate_token(user1)
    user1.token = response2.json()['token']
    user1.token_expires = response2.json()['expires']

    # WHEN
    response3 = api_helper.delete_user(user1)

    # THEN
    book_store_api.verify_code(response3, 204)


@allure.title('Verify successful token generation')
@allure.severity(Severity.BLOCKER)
def test_generate_token():
    # WHEN
    response = api_helper.generate_token(user2)

    # THEN
    book_store_api.verify_code(response, 200)
    book_store_api.verify_schema(response, 'post_token.json')
    book_store_api.verify_response_json(response, 'result', 'User authorized successfully.')
    book_store_api.verify_response_json(response, 'status', 'Success')


@allure.title('Verify receiving user information when user has a book added')
@allure.severity(Severity.BLOCKER)
def test_get_user_with_book():
    # GIVEN
    response1 = api_helper.generate_token(user3)
    user3.token = response1.json()['token']
    user3.token_expires = response1.json()['expires']
    book_store_api.verify_code(response1, 200)

    # WHEN
    response2 = api_helper.get_user(user3)

    # THEN
    book_store_api.verify_code(response2, 200)
    book_store_api.verify_response_json(response2, 'userId', user3.userid)
    book_store_api.verify_response_json(response2, 'username', user3.username)
    book_store_api.verify_json_books(response2, user3)
    book_store_api.verify_schema(response2, 'get_user.json')


@allure.title('Verify receiving user information when user has no books')
@allure.severity(Severity.BLOCKER)
def test_get_user_with_no_book():
    # GIVEN
    response1 = api_helper.generate_token(user4)
    user4.token = response1.json()['token']
    user4.token_expires = response1.json()['expires']
    book_store_api.verify_code(response1, 200)

    # WHEN
    response2 = api_helper.get_user(user4)

    # THEN
    book_store_api.verify_code(response2, 200)
    book_store_api.verify_response_json(response2, 'userId', user4.userid)
    book_store_api.verify_response_json(response2, 'username', user4.username)
    book_store_api.verify_json_books(response2, user4)
    book_store_api.verify_schema(response2, 'get_user.json')
