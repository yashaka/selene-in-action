import pytest
from selene import Browser, Config
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture()
def driver():
    """
    the original fixture to manage driver instance based on pure Selenium WebDriver
    """
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument('--headless=new')
    driver = webdriver.Chrome(
        service=ChromeService(executable_path=ChromeDriverManager().install()),
        options=driver_options,
    )

    yield driver

    driver.quit()


@pytest.fixture()
def browser(driver):
    """
    A fixture that we added later
    when decided to utilize Selene's power
    to stabilize Selenium-based tests
    """

    yield Browser(Config(driver=driver))
