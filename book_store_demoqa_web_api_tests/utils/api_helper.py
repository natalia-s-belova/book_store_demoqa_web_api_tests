import allure
from requests import sessions
from curlify import to_curl
from allure_commons.types import AttachmentType
import json
from book_store_demoqa_web_api_tests.data.users import User


def api_request(method, url, **kwargs):
    base_url = "https://demoqa.com"
    new_url = base_url + url
    with allure.step(f"{method.upper()} {new_url}"):
        with sessions.Session() as session:
            response = session.request(method=method, url=new_url, **kwargs)
            message = to_curl(response.request)
            allure.attach(body=message.encode("utf-8"), name="Curl", attachment_type=AttachmentType.TEXT,
                          extension='txt')
            if not response.content:
                allure.attach(body='empty response', name='Empty Response', attachment_type=AttachmentType.TEXT,
                              extension='txt')
            elif 'text/html' in response.headers['Content-Type']:
                allure.attach(body=response.content, name='Text/HTML Response', attachment_type=AttachmentType.TEXT,
                              extension='txt')
            elif 'application/json' in response.headers['Content-Type']:
                allure.attach(body=json.dumps(response.json(), indent=4).encode("utf-8"), name="Response Json",
                              attachment_type=AttachmentType.JSON, extension='json')
    return response


def response_schema(file_path):
    with open(file_path, encoding='utf-8') as file:
        schema = json.loads(file.read())
    return schema


def post_user(user: User):
    response = api_request(
        "post",
        url="/Account/v1/User",
        headers={"Content-Type": "application/json", "accept": "application/json"},
        data=json.dumps({'userName': user.username, 'password': user.password})
    )
    return response


def generate_token(user: User):
    response = api_request(
        "post",
        url="/Account/v1/GenerateToken",
        headers={"Content-Type": "application/json"},
        data=json.dumps({'userName': user.username, 'password': user.password})
    )
    return response


def get_user(user: User):
    response = api_request(
        "get",
        url=f"/Account/v1/User/{user.userid}",
        headers={"authorization": f"Bearer {user.token}"}
    )
    return response


def delete_user(user: User):
    response = api_request(
        "delete",
        url=f"/Account/v1/User/{user.userid}",
        headers={"authorization": f"Bearer {user.token}"}
    )
    return response


def get_book_info(isbn):
    response = api_request(
        "get",
        url=f"/BookStore/v1/Book",
        params={"ISBN": isbn}

    )
    return response


def add_books_for_user(isbns: list, user: User):
    lst_books = [{"isbn": isbn} for isbn in isbns]
    response = api_request(
        "post",
        url="/BookStore/v1/Books",
        data=json.dumps({"userId": user.userid,
                         "collectionOfIsbns": lst_books}),
        headers={"authorization": f"Bearer {user.token}", "Content-Type": "application/json"}
    )
    return response
