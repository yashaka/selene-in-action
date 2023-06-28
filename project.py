from typing import Literal
import dotenv
import pydantic


BrowserType = Literal['chrome', 'firefox', 'edge']


class Config(pydantic.BaseSettings):
    context: Literal['local', 'test', 'stage'] = 'local'

    base_url: str = 'https://todomvc.com/examples/emberjs'
    driver_name: BrowserType = 'chrome'
    hold_driver_at_exit: bool = False
    window_width: int = 1024
    window_height: int = 768
    timeout: float = 3.0
    headless: bool = False


# if you want to have optional .env file (without `.context` suffix)
# to allways override default values from .env.local, .env.test, .env.stage
# you may need it,
# as being ignored in .gitignore, – to store sensitive data (aka secrets)
dotenv.load_dotenv()
'''
# you may emphasize its "secrets" nature by naming it as .env.secrets:
dotenv.load_dotenv(dotenv.find_dotenv('.env.secrets'))
# sometimes people keep such secrets file outside of the project folder, 
# often – in home directory...
from pathlib import Path
dotenv.load_dotenv(Path.home().joinpath('.env.secrets').__str__())
'''

config = Config(dotenv.find_dotenv(f'.env.{Config().context}'))
'''
# if you would keep .env file name for local context (instead of .env.local)
context = Config().context
config = Config(dotenv.find_dotenv('.env' if context == 'local' else f'.env.{context}'

# another example, utilizing custom path helper from selene_in_action.utils.path
from selene_in_action.utils import path
config = Config(_env_file=path.relative_from_root(f'.env.{Config().context}'))
'''
