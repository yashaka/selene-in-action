import pytest
from selene import browser
import os


@pytest.fixture(scope='function', autouse=True)
def browser_management():
    browser.config.base_url = os.getenv(
        'selene.base_url', 'https://todomvc.com/examples/emberjs'
    )
    browser.config.browser_name = os.getenv('browser_name', 'chrome')
    browser.config.hold_browser_open = (
        os.getenv('hold_browser_open', 'false').lower() == 'true'
    )
    browser.config.window_width = os.getenv('window_width', '1024')
    browser.config.window_height = os.getenv('window_height', '768')
    browser.config.timeout = float(os.getenv('timeout', '3.0'))

    '''
    # Other Examples 
    # to make all clicks be performed via JavaScript 
    # * for cases when normal clicks does not work 
    browser.config.click_by_js = True  
    # ... but probably you don't want to «work around» all clicks.
    # to work-around just for specific elements you can do
    browser.element('#send').perform(command.js.click)
    # or if you need to repeat click via js a more than one time on same element:
    send = browser.element('#send').with_(click_by_js=True)
    send.click()
    ...
    send.click()
    # .with_(...) - is a special command that can be called on any Selene Entity
    # where Selene Entity is either:
    # * browser, 
    # * element, like browser.element(selector), browser.all(selector).first, etc.
    # * or collection, like browser.all(selector), browser.all(selector).by(condition), etc.
    # so you can call .with_ on any entity 
    # to customize any browser.config.* option 
    # for specific entity only, for example:
    # * browser.config.timeout = 10.0 will set global timeout to 10.0
    # but
    # * browser.all('.slow-list-item').with_(timeout=10.0) 
    #   will set such big timeout only for the specialized collection of slow list items

    # to make all type command calls to be performed via JavaScript 
    # ... for cases when normal clicks does not work 
    # ... or to speed up test execution (by faster typing)
    browser.config.type_by_js = True

    # setting driver instance manually for extra browser customization:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
    chrome_options = Options()
    chrome_options.headless = True  # ... like headless mode
    browser.config.driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=chrome_options
    )
    '''

    yield

    ...
