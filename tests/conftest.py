import pytest
from selene import browser
from selenium import webdriver

# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope='function', autouse=True)
def browser_management():
    browser.config.base_url = 'https://todomvc.com/examples/emberjs'
    browser.config.timeout = 2.0

    # browser.config.type_by_js = True
    '''
    ↑ if we would want to type text via JavaScript to speed up tests a bit
    '''

    # driver_options = webdriver.FirefoxOptions()
    '''
    ↑ if we would want to use Firefox with custom browser options instead of Chrome
    '''
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument('--headless=new')

    # browser.config.driver = webdriver.Chrome(
    #     service=ChromeService(executable_path=ChromeDriverManager().install()),
    #     options=driver_options,
    # )
    '''
    ↑ one day we need something like this for some complicated browser setup
    or support of some specific browser or driver
    ↓ but for now it's enough just to pass driver options to Selene's config
    '''
    browser.config.driver_options = driver_options

    yield

    browser.quit()
    '''
    ↑ Selene would automatically close browser for us in the very end of all tests
    but by we call browser.quit() explicitely after yield inside fixture of scope='function'
    so forcing browser to close after each test function for better tests independence ;)
    '''
