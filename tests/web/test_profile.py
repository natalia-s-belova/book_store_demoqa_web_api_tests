from book_store_demoqa_web_api_tests.models.web.profile import ProfilePage
from book_store_demoqa_web_api_tests.utils import actions_via_api
import allure
from allure_commons.types import Severity

pytestmark = [
    allure.label('layer', 'UI test'),
    allure.label('owner', 'natalia_belova'),
    allure.epic('BookStore Web'),
    allure.tag('web'),
    allure.feature('Profile')
]


@allure.title("Verify Profile when no books were added")
@allure.severity(Severity.CRITICAL)
def test_empty_profile(temp_user_management):
    # GIVEN
    user = temp_user_management()

    # WHEN
    profile_page = ProfilePage()
    profile_page.open()
    actions_via_api.login_via_api(user)

    # THEN
    profile_page.should_show_no_rows_message()


@allure.title("Verify Profile when user is not logged in")
@allure.severity(Severity.CRITICAL)
def test_logged_out_user():
    # WHEN
    profile_page = ProfilePage()
    profile_page.open()

    # THEN
    profile_page.verify_not_logged_in_message_shown()


@allure.title("Verify books in Profile correspond to previously added")
@allure.severity(Severity.BLOCKER)
def test_profile_with_books(temp_user_management):
    # GIVEN
    user = temp_user_management()
    profile_page = ProfilePage()
    profile_page.open()

    # WHEN
    actions_via_api.add_books_for_user(['9781449325862', '9781449331818'], user)
    actions_via_api.login_via_api(user)

    # THEN
    profile_page.should_have_exactly_books('Git Pocket Guide', 'Learning JavaScript Design Patterns')


@allure.title("Verify books search in Profile - book(s) are found")
@allure.severity(Severity.CRITICAL)
def test_search_for_existing_book_in_profile(temp_user_management):
    # GIVEN
    user = temp_user_management()
    profile_page = ProfilePage()
    profile_page.open()

    # WHEN
    actions_via_api.add_books_for_user(['9781449325862', '9781449331818'], user)
    actions_via_api.login_via_api(user)
    profile_page.enter_search_query('Git')

    # THEN
    profile_page.should_have_exactly_books('Git Pocket Guide')


@allure.title("Verify books search in Profile - book(s) are not found")
@allure.severity(Severity.CRITICAL)
def test_search_for_non_existing_book_in_profile(temp_user_management):
    # GIVEN
    user = temp_user_management()
    profile_page = ProfilePage()
    profile_page.open()

    # WHEN
    actions_via_api.add_books_for_user(['9781449325862', '9781449331818'], user)
    actions_via_api.login_via_api(user)
    profile_page.enter_search_query('Python')

    # THEN
    profile_page.should_have_exactly_books()
    profile_page.should_show_no_rows_message()


@allure.title("Verify user can delete one book from Profile")
@allure.severity(Severity.CRITICAL)
def test_delete_one_book(temp_user_management):
    # GIVEN
    user = temp_user_management()
    profile_page = ProfilePage()
    profile_page.open()

    # WHEN
    actions_via_api.add_books_for_user(['9781449325862', '9781449331818'], user)
    actions_via_api.login_via_api(user)
    profile_page.should_have_exactly_books('Git Pocket Guide', 'Learning JavaScript Design Patterns')
    profile_page.delete_book_in_the_list_no(0)

    # THEN
    profile_page.should_have_exactly_books('Learning JavaScript Design Patterns')


@allure.title("Verify user can delete all books from Profile")
@allure.severity(Severity.CRITICAL)
def test_delete_all_books(temp_user_management):
    # GIVEN
    user = temp_user_management()
    profile_page = ProfilePage()
    profile_page.open()

    # WHEN
    actions_via_api.add_books_for_user(['9781449325862', '9781449331818'], user)
    actions_via_api.login_via_api(user)
    profile_page.should_have_exactly_books('Git Pocket Guide', 'Learning JavaScript Design Patterns')
    profile_page.delete_all_books()

    # THEN
    profile_page.should_have_exactly_books()
    profile_page.should_show_no_rows_message()
