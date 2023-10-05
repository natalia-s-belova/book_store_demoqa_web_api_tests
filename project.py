import dotenv
import pydantic_settings
from typing import Literal

BrowserType = Literal['chrome', 'firefox']


class Config(pydantic_settings.BaseSettings):
    driver_name: BrowserType = 'firefox'
    browser_version: str = '98.0'
    hold_driver_at_exit: bool = False
    base_url: str = 'https://demoqa.com'
    window_width: int = 1920
    window_height: int = 1080
    timeout: float = 3.0
    login: str
    password: str


config = Config(_env_file=dotenv.find_dotenv('.env'))
