from selene import have
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

# from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.support.wait import WebDriverWait


def test_complete_todo(driver, browser):
    """
    An example of test implemented with pure Selenium WebDriver
    with further changes of utilizing Selene's browser
    to stabilize test and make it more readable
    """

    driver.get('https://todomvc.com/examples/emberjs')
    # assert driver.find_element(By.CSS_SELECTOR, '#new-todo').get_attribute('value') == ''
    browser.element('#new-todo').should(have.value(''))
    '''
    ↑ stabilizing assertion
    '''

    # driver.find_element(By.CSS_SELECTOR, '#new-todo').send_keys('a' + Keys.ENTER)
    browser.element('#new-todo').send_keys('a' + Keys.ENTER)
    '''
    ↑ stabilizing interaction with first element
    '''
    driver.find_element(By.CSS_SELECTOR, '#new-todo').send_keys('b' + Keys.ENTER)
    driver.find_element(By.CSS_SELECTOR, '#new-todo').send_keys('c' + Keys.ENTER)
    '''
    ↑ some lines can be left as implemented in pure Selenium WebDriver
    - without conflicts with Selene ;)
    '''
    # WebDriverWait(driver=browser.driver, timeout=3.0).until(
    #     lambda driver: len(driver.find_elements(By.CSS_SELECTOR, '#todo-list>li') == 3)
    # )
    browser.all('#todo-list>li').should(have.exact_texts('a', 'b', 'c'))
    '''
    ↑ making explicit-wait-like assertion more readable,
    with better error messages,
    and more powerful by asserting not just size of list,
    but texts of elements and their order
    '''

    ...
