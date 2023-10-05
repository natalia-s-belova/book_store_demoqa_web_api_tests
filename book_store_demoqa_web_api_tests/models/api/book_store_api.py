import jsonschema
import allure
from book_store_demoqa_web_api_tests.utils import api_helper, path
from book_store_demoqa_web_api_tests.data.users import User


def verify_code(response, code):
    with allure.step(f'Verify response code is {code}'):
        assert response.status_code == code


def verify_schema(response, file_name):
    with allure.step('Verify response schema'):
        schema = api_helper.response_schema(path.path_dir('api', 'resources', 'schemas', file_name))
        jsonschema.validators.validate(instance=response.json(), schema=schema)


def verify_response_json(response, parameter, value):
    with allure.step(f'Verify response json contains "{parameter}" = {value}'):
        assert response.json()[parameter] == value


def verify_response_text_is_blank(response):
    with allure.step('Verify response text is blank'):
        assert response.text == ''


def verify_json_books(response, user: User):
    with allure.step('Verify books in response'):
        assert response.json()['books'] == user.books
