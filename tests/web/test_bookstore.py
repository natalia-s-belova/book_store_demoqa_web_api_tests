import project
from book_store_demoqa_web_api_tests.models.web.book_store import BooksPage
from book_store_demoqa_web_api_tests.utils import actions_via_api
import pytest
import allure
from allure_commons.types import Severity

pytestmark = [
    allure.label('layer', 'UI test'),
    allure.label('owner', 'natalia_belova'),
    allure.epic('BookStore Web'),
    allure.tag('web'),
    allure.feature('Books')
]


@allure.title('Verify successful search by books title')
@allure.severity(Severity.CRITICAL)
def test_search_found():
    # GIVEN
    books_page = BooksPage()
    books_page.open()
    books_page.should_have_exactly_books('Git Pocket Guide', 'Learning JavaScript Design Patterns',
                                         'Designing Evolvable Web APIs with ASP.NET',
                                         'Speaking JavaScript', "You Don't Know JS",
                                         'Programming JavaScript Applications',
                                         'Eloquent JavaScript, Second Edition',
                                         'Understanding ECMAScript 6')

    # WHEN
    books_page.enter_search_query('JavaScript')

    # THEN
    books_page.should_have_exactly_books('Learning JavaScript Design Patterns', 'Speaking JavaScript',
                                         'Programming JavaScript Applications',
                                         'Eloquent JavaScript, Second Edition')


@allure.title('Verify search by books title - nothing found')
@allure.severity(Severity.CRITICAL)
def test_search_not_found():
    # GIVEN
    books_page = BooksPage()
    books_page.open()

    # WHEN
    books_page.enter_search_query('Python')

    # THEN
    books_page.should_have_exactly_books()
    books_page.should_show_no_rows_message()


@allure.title('Verify Book Details page')
@allure.severity(Severity.BLOCKER)
def test_open_book_details_logged_out():
    # GIVEN
    books_page = BooksPage()
    books_page.open()

    # WHEN
    books_page.click_book_title('Git Pocket Guide')

    # THEN
    books_page.verify_book_details_shown('Git Pocket Guide')


@allure.title('Verify going from Book Details to Books List')
@allure.severity(Severity.NORMAL)
def test_go_back_to_books_list():
    # GIVEN
    books_page = BooksPage()
    books_page.open()

    books_page.click_book_title('Git Pocket Guide')
    books_page.verify_book_details_shown('Git Pocket Guide')

    # WHEN
    books_page.click_go_back_to_books_store()

    # THEN
    books_page.verify_books_list_page_opened()


@allure.title('Verify going from Books List to Login')
@allure.severity(Severity.NORMAL)
def test_go_to_login_from_books_list():
    # GIVEN
    books_page = BooksPage()
    books_page.open()

    # WHEN
    books_page.click_login()

    # THEN
    books_page.verify_login_page_opened()


@allure.title('Verify going from Book Details to Login')
@allure.severity(Severity.NORMAL)
def test_go_to_login_from_book_details():
    # GIVEN
    books_page = BooksPage()
    books_page.open()
    books_page.click_book_title('Git Pocket Guide')

    # WHEN
    books_page.click_login()

    # THEN
    books_page.verify_login_page_opened()


@allure.title("Verify adding of a book to user's collection")
@allure.severity(Severity.CRITICAL)
def test_add_book_to_collection(temp_user_management):
    if project.config.driver_name == 'chrome':
        pytest.skip('Selenoid issue: alerts interactions causes nginx timeout error. Rerun on Firefox or locally.')

    # GIVEN
    user = temp_user_management()

    books_page = BooksPage()
    books_page.open()
    actions_via_api.login_via_api(user)

    # WHEN
    books_page.click_book_title('Learning JavaScript Design Patterns')
    books_page.click_add_to_collection()

    # THEN
    books_page.verify_alert_text_and_accept('Book added to your collection.')
    actions_via_api.verify_books_list_via_api(user,
                                              [{'isbn': '9781449331818', 'title': 'Learning JavaScript Design Patterns',
                                                'subTitle': "A JavaScript and jQuery Developer's Guide",
                                                'author': 'Addy Osmani', 'publish_date': '2020-06-04T09:11:40.000Z',
                                                'publisher': "O'Reilly Media", 'pages': 254,
                                                'description': "With Learning JavaScript Design Patterns, you'll learn how to write beautiful, structured, and maintainable JavaScript by applying classical and modern design patterns to the language. If you want to keep your code efficient, more manageable, and up-to-da",
                                                'website': 'http://www.addyosmani.com/resources/essentialjsdesignpatterns/book/'}])


@allure.title("Verify adding book that has already been added to user's collection")
@allure.severity(Severity.CRITICAL)
def test_add_book_to_collection_already_exists(temp_user_management):
    if project.config.driver_name == 'chrome':
        pytest.skip('Selenoid issue: alerts interactions causes nginx timeout error. Rerun on Firefox or locally.')

    # GIVEN
    user = temp_user_management()

    books_page = BooksPage()
    books_page.open()
    actions_via_api.login_via_api(user)

    # WHEN
    books_page.click_book_title('Learning JavaScript Design Patterns')
    books_page.click_add_to_collection()
    books_page.verify_alert_text_and_accept('Book added to your collection.')
    books_page.click_add_to_collection()

    # THEN
    books_page.verify_alert_text_and_accept('Book already present in the your collection!')
    actions_via_api.verify_books_list_via_api(user,
                                              [{'isbn': '9781449331818', 'title': 'Learning JavaScript Design Patterns',
                                                'subTitle': "A JavaScript and jQuery Developer's Guide",
                                                'author': 'Addy Osmani', 'publish_date': '2020-06-04T09:11:40.000Z',
                                                'publisher': "O'Reilly Media", 'pages': 254,
                                                'description': "With Learning JavaScript Design Patterns, you'll learn how to write beautiful, structured, and maintainable JavaScript by applying classical and modern design patterns to the language. If you want to keep your code efficient, more manageable, and up-to-da",
                                                'website': 'http://www.addyosmani.com/resources/essentialjsdesignpatterns/book/'}])
