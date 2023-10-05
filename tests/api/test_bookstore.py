from book_store_demoqa_web_api_tests.utils import api_helper
from book_store_demoqa_web_api_tests.models.api import book_store_api
from book_store_demoqa_web_api_tests.data.users import User
import allure
from allure_commons.types import Severity

user = User(username='temp_api_testing_user', password='Test1234!')

pytestmark = [
    allure.label('layer', 'API test'),
    allure.label('owner', 'natalia_belova'),
    allure.epic('BookStore API'),
    allure.tag('REST'),
    allure.feature('Books')
]


@allure.title('Verify adding of a single book for a user')
@allure.severity(Severity.BLOCKER)
def test_add_book_for_user():
    # GIVEN
    response_create_user = api_helper.post_user(user)
    user.userid = response_create_user.json()['userID']

    response_generate_token = api_helper.generate_token(user)
    user.token = response_generate_token.json()['token']
    user.token_expires = response_generate_token.json()['expires']

    response_get_user = api_helper.get_user(user)
    book_store_api.verify_response_json(response_get_user, 'books', [])

    # WHEN
    response_add_book = api_helper.add_books_for_user(['9781449325862'], user)

    # THEN
    book_store_api.verify_code(response_add_book, 201)
    book_store_api.verify_schema(response_add_book, 'add_book.json')

    # WHEN
    response_get_user_2 = api_helper.get_user(user)

    # THEN
    book_store_api.verify_response_json(response_get_user_2, 'books', [{
        "isbn": "9781449325862",
        "title": "Git Pocket Guide",
        "subTitle": "A Working Introduction",
        "author": "Richard E. Silverman",
        "publish_date": "2020-06-04T08:48:39.000Z",
        "publisher": "O'Reilly Media",
        "pages": 234,
        "description": "This pocket guide is the perfect on-the-job companion to Git, the distributed version control system. It provides a compact, readable introduction to Git for new users, as well as a reference to common commands and procedures for those of you with Git exp",
        "website": "http://chimera.labs.oreilly.com/books/1230000000561/index.html"}])

    api_helper.delete_user(user)


@allure.title('Verify adding of a several books for a user')
@allure.severity(Severity.BLOCKER)
def test_add_several_books_for_user():
    # GIVEN
    response_create_user = api_helper.post_user(user)
    user.userid = response_create_user.json()['userID']

    response_generate_token = api_helper.generate_token(user)
    user.token = response_generate_token.json()['token']
    user.token_expires = response_generate_token.json()['expires']

    response_get_user = api_helper.get_user(user)
    book_store_api.verify_response_json(response_get_user, 'books', [])

    # WHEN
    response_add_books = api_helper.add_books_for_user(['9781449325862', '9781449365035'], user)

    # THEN
    book_store_api.verify_code(response_add_books, 201)
    book_store_api.verify_schema(response_add_books, 'add_book.json')

    # WHEN
    response_get_user_2 = api_helper.get_user(user)

    # THEN
    book_store_api.verify_response_json(response_get_user_2, 'books', [
        {
            "isbn": "9781449325862",
            "title": "Git Pocket Guide",
            "subTitle": "A Working Introduction",
            "author": "Richard E. Silverman",
            "publish_date": "2020-06-04T08:48:39.000Z",
            "publisher": "O'Reilly Media",
            "pages": 234,
            "description": "This pocket guide is the perfect on-the-job companion to Git, the distributed version control system. It provides a compact, readable introduction to Git for new users, as well as a reference to common commands and procedures for those of you with Git exp",
            "website": "http://chimera.labs.oreilly.com/books/1230000000561/index.html"
        },
        {
            "isbn": "9781449365035",
            "title": "Speaking JavaScript",
            "subTitle": "An In-Depth Guide for Programmers",
            "author": "Axel Rauschmayer",
            "publish_date": "2014-02-01T00:00:00.000Z",
            "publisher": "O'Reilly Media",
            "pages": 460,
            "description": "Like it or not, JavaScript is everywhere these days-from browser to server to mobile-and now you, too, need to learn the language or dive deeper than you have. This concise book guides you into and through JavaScript, written by a veteran programmer who o",
            "website": "http://speakingjs.com/"
        }
    ])

    api_helper.delete_user(user)


@allure.title('Verify receiving book details')
@allure.severity(Severity.BLOCKER)
def test_get_book_info():
    # GIVEN
    isbn = '9781449325862'

    # WHEN
    response = api_helper.get_book_info(isbn)

    # THEN
    book_store_api.verify_code(response, 200)
    book_store_api.verify_schema(response, 'get_book.json')
    book_store_api.verify_response_json(response, 'isbn', isbn)
    book_store_api.verify_response_json(response, 'title', 'Git Pocket Guide')
    book_store_api.verify_response_json(response, 'subTitle', 'A Working Introduction')
