from selene import browser, have


def test_add_todos_and_complete_one():
    browser.open('/')
    browser.should(have.title_containing('TodoMVC'))

    browser.element('#new-todo').type('a.').press_enter()
    browser.element('#new-todo').type('b.').press_enter()
    browser.element('#new-todo').type('c.').press_enter()
    browser.element('#new-todo').type('d.').press_enter()
    browser.all('#todo-list>li').should(have.exact_texts('a.', 'b.', 'c.', 'd.'))

    browser.all('#todo-list>li').element_by(have.exact_text('b.')).element(
        '.toggle'
    ).click()
    browser.all('#todo-list>li').by(have.css_class('completed')).should(
        have.exact_texts('b.')
    )
    browser.all('#todo-list>li').by(have.no.css_class('completed')).should(
        have.exact_texts('a.', 'c.', 'd.')
    )
