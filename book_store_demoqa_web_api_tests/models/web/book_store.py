from selene import browser, have, command
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class BooksPage:

    def open(self):
        with allure.step('Open Book Store page'):
            browser.open('/books')
            browser.all('[id^=google_ads][id$=container__]').with_(timeout=10).wait_until(
                have.size_greater_than_or_equal(3)
            )
            browser.all('[id^=google_ads][id$=container__]').perform(command.js.remove)

    def should_have_exactly_books(self, *books_titles):
        with allure.step(f'Verify books titles: {books_titles}'):
            browser.all('[id^=see-book]').should(
                have.exact_texts(books_titles))

    def should_show_no_rows_message(self):
        with allure.step('Verify No Rows message is present'):
            browser.element('.rt-noData').should(have.exact_text('No rows found'))

    def click_book_title(self, title):
        with allure.step(f'Click title: {title}'):
            browser.all('[id^=see-book]').element_by(have.exact_text(title)).click()

    def verify_book_details_shown(self, title):
        with allure.step(f'Verify book details is opened for: {title}'):
            browser.should(have.url_containing('https://demoqa.com/books?book='))
            browser.element('#title-wrapper #userName-value').should(have.exact_text(title))

    def verify_books_list_page_opened(self):
        with allure.step('Verify books list page is opened'):
            browser.should(have.url('https://demoqa.com/books'))

    def click_go_back_to_books_store(self):
        with allure.step('Click Go back to Store'):
            browser.all('#addNewRecordButton').element_by(have.exact_text('Back To Book Store')).click()

    def click_add_to_collection(self):
        with allure.step('Click Add to collection'):
            browser.all('#addNewRecordButton').element_by(have.exact_text('Add To Your Collection')).click()

    def verify_alert_text_and_accept(self, alert_text):
        with allure.step(f'Verify alert with "{alert_text}" is shown'):
            WebDriverWait(browser, 10).until(EC.alert_is_present(),
                                             'Timed out waiting for PA creation ' +
                                             'confirmation popup to appear.')
            alert = browser.switch_to.alert
            assert alert.text == alert_text
        with allure.step('Accept alert'):
            alert.accept()

    def click_login(self):
        with allure.step('Click Login button'):
            browser.element('#login').click()

    def verify_login_page_opened(self):
        with allure.step('Verify Login page is opened'):
            browser.should(have.url('https://demoqa.com/login'))

    def enter_search_query(self, text):
        with allure.step(f'Enter "{text}" to search line'):
            browser.element('#searchBox').type(text)
