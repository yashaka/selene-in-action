import pytest
from selene import browser
from selenium import webdriver

import project


@pytest.fixture(scope='function', autouse=True)
def browser_management():
    browser.config.base_url = project.config.base_url
    browser.config.driver_name = project.config.driver_name
    browser.config.hold_driver_at_exit = project.config.hold_driver_at_exit
    browser.config.window_width = project.config.window_width
    browser.config.window_height = project.config.window_height
    browser.config.timeout = project.config.timeout

    if project.config.headless:
        if project.config.driver_name == 'edge':
            raise ValueError('Edge does not support headless mode')
        driver_options = (
            webdriver.ChromeOptions()
            if project.config.driver_name == 'chrome'
            else webdriver.FirefoxOptions()
        )
        driver_options.add_argument('--headless=new')
        browser.config.driver_options = driver_options

    yield

    ...
