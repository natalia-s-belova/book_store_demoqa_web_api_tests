from selene import browser, have, command
import allure


class ProfilePage:

    def open(self):
        with allure.step('Open Profile page'):
            browser.open('/profile')
            browser.all('[id^=google_ads][id$=container__]').with_(timeout=10).wait_until(
                have.size_greater_than_or_equal(3)
            )
            browser.all('[id^=google_ads][id$=container__]').perform(command.js.remove)

    def should_show_no_rows_message(self):
        with allure.step('Verify No Rows message is present'):
            browser.element('.rt-noData').should(have.exact_text('No rows found'))

    def verify_not_logged_in_message_shown(self):
        with allure.step('Verify Not Logged in message is present'):
            browser.element('#notLoggin-label').should(
                have.text(
                    'Currently you are not logged into the Book Store application, please visit the login page to enter or register page to register yourself.'))

    def should_have_exactly_books(self, *books_titles):
        with allure.step(f'Verify books are present: {books_titles}'):
            browser.all('[id^=see-book]').should(
                have.exact_texts(books_titles))

    def enter_search_query(self, text):
        with allure.step(f'Enter "{text}" to search line'):
            browser.element('#searchBox').type(text)

    def delete_book_in_the_list_no(self, order):
        with allure.step(f'Delete book number {order+1}'):
            browser.all('#delete-record-undefined')[order].click()
            browser.element('#closeSmallModal-ok').click()

    def delete_all_books(self):
        with allure.step(f"Delete all user's books"):
            browser.all('#submit')[2].click()
            browser.element('#closeSmallModal-ok').click()
