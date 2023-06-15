from selene.support.conditions.be import *  # noqa
from selene.support.conditions.have import *  # noqa

'''
# ↑ here we import all conditions from selene.support.conditions
# just in case you don't like to use two separate modules for conditions:

from selene import have, be
browser.element('#new-todo').should(be.blank)
browser.all('#todo-list>li').should(have.size(3))

# but want just one:

from selene_in_action.conditions import match
browser.element('#new-todo').should(match.blank)
browser.all('#todo-list>li').should(match.size(3))
'''
