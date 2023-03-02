from selene import browser, have, be, command, query, by

'''
# imports for custom driver setup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
'''

'''
# imports for extra chainable actions, like simulating «Command/Ctrl + a»
from selenium.webdriver import ActionChains, Keys
'''


def test_add_todos_and_complete_one():

    # browser.config.hold_browser_open = True
    browser.config.window_width = '1024'
    browser.config.window_height = '768'
    browser.config.timeout = 6.0
    '''
    browser.config.browser_name = 'firefox'
    
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
    # not available in selene ~ 2.0.0b17, but will be added soon:
    browser.config.desired_capabilities = chrome_options
    '''

    browser.open('https://todomvc.com/examples/emberjs/')
    browser.should(have.title_containing('TodoMVC'))
    '''
    # example of running any custom JavaScript in browser
    browser.execute_script('document.querySelector("#new-todo").remove()') # for stupid reason:)
    # ... but sometimes you will need to remove something «more important» :D
    # same can be done by:
    browser.driver.execute_script('document.querySelector("#new-todo").remove()')
    # another style of executing script to achieve same goal as above but shorter:
    browser.element('#new-todo').execute_script('element.remove()')
    # using selenium webdriver style you would do the same by:
    webelement = browser.element('#new-todo').locate()
    browser.driver.execute_script('arguments[0].remove()', webelement)
    # – that is much less concise of course ;)
    
    # above... the browser.element('#new-todo').locate() 
    # is a Selene's shortcut for Selenium's:
    from selenium.webdriver.common.by import By
    browser.driver.find_element(By.CSS_SELECTOR, '#new-todo')
    # you may also encounter, especially in Selene's own sources something like this:
    webelement = browser.element('#new-todo')()
    # or
    element = browser.element('#new-todo')
    webelement = element() 
    # – all this – is same as calling explicitly:
    webelement = element.locate() 
    # ;)
    
    '''

    browser.element('#new-todo').type('a.').press_enter()
    browser.element('#new-todo').type('b.').press_enter()
    browser.element('#new-todo').type('c.').press_enter()
    browser.element('#new-todo').type('d.').press_enter()
    '''
    # just example of different type of selectors/locators you can use
    # css selectors are the simplest:
    browser.element('#new-todo').type('a.').press_enter()
    # selenium style of locators:
    new_todo_locator = By.CSS_SELECTOR, '#new-todo'
    browser.element(new_todo_locator).type('b.').press_enter()
    # but Selene has a shortcut for such «tuple-like locator»
    browser.element(by.id('new-todo')).type('c.').press_enter()
    # xpath also works:
    browser.element('//*[@id="new-todo"]').type('d.').press_enter()
    
    # Sometimes you need to simulate something not ordinary with Selenium's ActionChains
    from selenium.webdriver import ActionChains, Keys
    browser.element('#new-todo').type('originally typed text...')
    actions = ActionChains(browser.driver)
    actions.key_down(Keys.COMMAND).send_keys('a').key_up(Keys.COMMAND).perform()
    browser.element('#new-todo').type('this task will overwrite original')
    
    # now let's check assertions...
    # given...
    browser.open('https://todomvc.com/examples/emberjs/')
    browser.element('#new-todo').type('foo bar kuka riku').press_enter()
    # probably you are used to assert the result by something like this:
    text = browser.element('#todo-list>li').locate().text  # => 'foo bar kuka riku'
    # or a bit more stable (because .get(...) will wait till element is available at least in DOM)
    text = browser.element('#todo-list>li').get(query.text)  # => 'foo bar kuka riku'
    assert 'foo' in text  # <- but this
    assert 'kuka' in text  # <- and this
    # will not wait till corresponding text will appear in modern-dynamic-often-slow-loading web app

    # But in Selene, though a bit slower, but much more stable would be:
    browser.element('#todo-list>li').should(have.text('foo')).should(have.text('kuka'))
    # Remember, in the End to End testing of already pretty slow modern web applications,
    # we value stability more than speed of execution.
    # And yet you can do it with same speed as «assert ...» version
    browser.element('#todo-list>li').should(have.text('foo').and_(have.text('kuka'))
    # – All this is much more stable, because .should knows how to wait till exact needed text appears
    # ... and you never know when your app will load longer than your script executes the code
    
    # Yet, listen... even 
    browser.element('#todo-list>li').should(have.text('foo'))
    # – is not the best option that we can use to assert todos that we created in the test... 
    # – much more efficient would be ... 
    '''
    browser.all('#todo-list>li').should(have.exact_texts('a.', 'b.', 'c.', 'd.'))
    '''
    # – that is a shortcut for
    browser.all('#todo-list>li').should(have.size(4))
    browser.all('#todo-list>li')[0].should(have.exact_text('a.')
    browser.all('#todo-list>li')[1].should(have.exact_text('b.')
    browser.all('#todo-list>li')[2].should(have.exact_text('c.')
    browser.all('#todo-list>li')[3].should(have.exact_text('d.')
    # ... i.e will do 3 assertions at once: 
    # 1 exact texts of each todo in the list (by exact equality)
    # 2 todos exact size
    # 3 todos exact order
    # other option might be:
    browser.all('#todo-list>li').should(have.texts('a', 'b', 'c', 'd'))
    # – that will assert texts «by contains» (not by exact equality)

    # And here are more examples of assertions applied to «filtered collection of todos»
    browser.all('#todo-list>li')[2].should(have.exact_text('c.'))
    browser.all('#todo-list>li')[1:3].should(have.texts('b', 'c'))
    browser.all('#todo-list>li').first.should(have.exact_text('a.'))
    browser.all('#todo-list>li').second.should(have.exact_text('b.'))
    browser.all('#todo-list>li')[-1].should(have.exact_text('d.'))
    browser.all('#todo-list>li').even.should(have.exact_texts('b.', 'd.'))
    browser.all('#todo-list>li').odd.should(have.exact_texts('a.', 'c.'))
    '''

    browser.all('#todo-list>li').element_by(have.exact_text('b.')).element(
        '.toggle'
    ).click()
    browser.all('#todo-list>li').by(have.css_class('completed')).should(
        have.exact_texts('b.')
    )
    browser.all('#todo-list>li').by(have.no.css_class('completed')).should(
        have.exact_texts('a.', 'c.', 'd.')
    )

    '''
    # Here are a few examples of some complex Selene Locators... 
    # (you can consider a chain of selene's commands to filter original browser.all(selector) 
    # – a «Selene's Locator»
    # For example, this is a normal Selene Collection 
    # or in other words a simple Selene's Locator based on '#todo-list>li input' css selector:
    browser.all('#todo-list>li input')
    # and here is same but more complex, composite Selene's Locator, 
    # that is a broken down version of the previous one:
    browser.all('#todo-list>li').all('input')
    # ... you can see that they are same by checking the size of the result collection:
    browser.all('#todo-list>li input').should(have.size(6))
    browser.all('#todo-list>li').all('input').should(have.size(6))
    # while this will be a bit different:
    browser.all('#todo-list>li').all_first('input').should(have.size(3))
    # and similar to:
    browser.all('#todo-list>li .toggle').should(have.size(3))
    
    # Notice, that Selene allows to break down "longer css selectors" into parts...
    # By this, sometimes we get more code, but this code is still pretty readable,
    # and what's the main point of this – it allows better support later.
    # When for example such code fail:
    browser.all('#todo-list>li').element_by(have.exact_text('>b.')).element(
        '.toggle'
    ).click()
    # we see in the error ...
    #
    # E    Timed out after 6.0s, while waiting for:
    # E    browser.all(('css selector', '#todo-list>li')).element_by(has exact text >b.).element(('css selector', '.toggle')).click
    # E    
    # E    Reason: AssertionError: 
    # E    	Cannot find element by condition «has exact text >b.» 
    # E    	Among browser.all(('css selector', '#todo-list>li'))
    # 
    # ... – that exactly the .element_by(have.exact_text('>b.')) part did not work!
    # otherwise (in case of unbroken-down-css-selector (or xpath) 
    # it would be harder to find the cause quickly
    # This is one of the strongest point of Selene, when comparing to raw Selenium ;)
    
    # And here are some more extraordinary cases...
    # Given after completing a todo 
    # – its .toggle checkbox has 'selected' attribute (in reality this is not true, 
    # but let's imagine this...)
    # Then this is how we can filter todos by their inner .toggle element matching needed condition
    # in order to e.g. remove the task by other inner element:
    browser.all('#todo-list>li').element_by_its('.toggle', have.attribute('selected')).element('.remove').click()
    # (in reality there is not 'remove' css class name, but if it would be... just imagine ;) )
    # or another example of pretty often use case:
    browser.all('.teacher').element_by_its('.firstName', have.text('Yasha')).element(
        '.go-to-sleep'
    ).click()
    
    # more examples, just for fun ;)
    for student in browser.all('.student'):
        student.element('.go-to-sleep').click()

    for bad_guy in browser.all('.bad-guy'):
        bad_guy.element('.remove-from-earth').perform(command.js.click)
        
    # but notice, that usually we don't use loops like a for-loop in tests
    # it's a bad practice to use any complex programming language features in tests
    # tests should be simple (i.e. KISS!)
    '''
