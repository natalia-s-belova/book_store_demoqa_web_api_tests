from dataclasses import dataclass
from typing import List


@dataclass
class User:
    username: str
    password: str
    userid: str = ''
    token: str = ''
    token_expires: str = ''
    books: list = List
