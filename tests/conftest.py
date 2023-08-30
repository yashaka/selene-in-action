import pytest
from selene import browser
import os


@pytest.fixture(scope='function', autouse=True)
def browser_management():
    browser.config.base_url = os.getenv(
        'base_url', 'https://www.wikipedia.org'
    )
    browser.config.driver_name = os.getenv('driver_name', 'chrome')
    browser.config.hold_driver_at_exit = (
        os.getenv('hold_driver_at_exit', 'false').lower() == 'true'
    )
    browser.config.window_width = os.getenv('window_width', '1024')
    browser.config.window_height = os.getenv('window_height', '768')
    browser.config.timeout = float(os.getenv('timeout', '3.0'))

    yield

    ...
