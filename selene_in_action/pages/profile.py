from selene import browser

import project


class Profile:
    """
    Just an example of some PageObject,
    from where we can also access pydantic-based project.config
    """

    def save(self):
        if project.config.context == 'stage':
            browser.driver.switch_to.alert.accept()

        browser.element('#save').click()
