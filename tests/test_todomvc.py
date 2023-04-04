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

    browser.open('/')
    browser.should(have.title_containing('TodoMVC'))
    '''
    # .should(condition) is a Selene's version of «explicit wait» that is mainly used as «waiting assertion»
    # If condition passed to it – is matched – the should command PASSES 
    # ELSE – the should command raise an Error i.e. FAILS
    #        if during browser.config.timeout period of time the condition still is not matched
    # Hence, should – always waits by config.timeout till condition passes, and if not – raise an Error
    # .should has the following siblings with following differences:
    # * .wait_until(condition), 
    #   – that has same behavior but instead of raising an Error once failed to match – returns False
    #     i.e. it also waits like .should but in all scenarios will not fail the test
    # * .matching(condition)
    #   - same as .wait_until but does not wait,
    #     i.e. checks the condition and returns True or False correspondingly
    # you might need .wait_until or .matching to implement some branching logic in a test
    # as some workaround (because branching is bad practice in Tests Code)
    # Example:
    if browser.matching(have.no.title('TodoMvc')):
        print('Developers went crazy again and screwed up my favorite app title :`(')
    
    if browser.wait_until(have.title('TodoMvc')):
        print('Yahoo!!! Devs left my day shiny today, I can relax watching my favourite app title')
    # More useful example:
    if browser.element(
        '#crazy-alert-that-appears-sometimes-and-sometimes-not'
    ).wait_until(be.visible):
        browser.element('#close-crazy-alert').click()
    
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
    from selenium.webdriver.common.by import By

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
    # (use Keys.CONTROL for windows,
    # google for receipt on how to make the code a crossplatform;))
    #
    # ... It's interesting though, that you can do same without actions...
    # simply by typing:
    browser.element('#new-todo').type(Keys.COMMAND + 'a')
    # just the Keys.COMMAND will remain «not released»,
    # but you can simulate «release everything» by Keys.NULL:
    browser.element('#new-todo').type(Keys.COMMAND + 'a' + Keys.NULL)
    # Hence, if you need to rewrite previous test by simulating «ctrl/command + a»
    # you can do:
    browser.element('#new-todo').type(
        Keys.COMMAND + 'a' + Keys.NULL + 'this task will overwrite original'
    )
    # or same but passing a few parameters at once:
    browser.element('#new-todo').send_keys(
        Keys.COMMAND + 'a', Keys.NULL, 'this task will overwrite original'
    )
    # or formatted in a more readable way:
    release_keys = Keys.NULL
    browser.element('#new-todo').send_keys(
        Keys.COMMAND + 'a',
        release_keys,
        'this task will overwrite original',
    )

    # .send_keys(*values) – is kind of «low-level typing simulation»,
    # that allows to provide a few «values» separated by comma
    # .send_keys is also a good candidate to use to upload a file:
    browser.element('input[type=file]').send_keys('/Users/yashaka/avatar.png')
    # 'input[type=file]' might be not the best selector, probably you'll have something like:
    browser.element('#fild-upload').send_keys('/Users/your/avatar.png')

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
    browser.element('#todo-list>li').should(have.text('foo').and_(have.text('kuka')))
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
