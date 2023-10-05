import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene import browser
from book_store_demoqa_web_api_tests.utils import attach
import project
from book_store_demoqa_web_api_tests.utils import actions_via_api
from book_store_demoqa_web_api_tests.data.users import User


@pytest.fixture(scope='function', autouse=True)
def setup_browser():
    browser.config.base_url = project.config.base_url
    browser.config.window_width = project.config.window_width
    browser.config.window_height = project.config.window_height
    browser.config.timeout = project.config.timeout

    options = Options()
    selenoid_capabilities = {
        "browserName": project.config.driver_name,
        "browserVersion": project.config.browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor=f"https://{project.config.login}:{project.config.password}@selenoid.autotests.cloud/wd/hub",
        options=options
    )

    browser.config.driver = driver

    yield browser

    attach.add_html(browser)
    attach.add_screenshot(browser)
    if project.config.driver_name == 'chrome':
        attach.add_logs(browser)
    attach.add_video(browser)
    browser.quit()


@pytest.fixture()
def temp_user_management():
    user_temp = User(username='temp_user_for_web_testing', password='Test123!')

    def generate_user():
        user = actions_via_api.create_account_via_api(user_temp)
        return user

    yield generate_user
    actions_via_api.delete_acc_via_api(user_temp)
