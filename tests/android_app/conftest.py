import allure
import pytest
import allure_commons
from appium.options.android import UiAutomator2Options
from selene import browser, support
import os

import config
from selene_in_action import utils

from appium import webdriver


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote(
            config.remote_url,
            options=config.to_driver_options()
        )

    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield

    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=allure.attachment_type.PNG,
    )

    allure.attach(
        browser.driver.page_source,
        name='screen xml dump',
        attachment_type=allure.attachment_type.XML,
    )

    session_id = browser.driver.session_id

    with allure.step('tear down app session with id: ' + session_id):
        browser.quit()

    if config.runs_on_bstack:
        utils.allure.attach_bstack_video(session_id)
