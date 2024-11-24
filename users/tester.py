import os

from dotenv import load_dotenv

from firebot import fire_bot_worker
from firebot.users import USERS

load_dotenv()

user = USERS(name='tester',
             token=os.getenv('TESTER'),
             web_hook_url=os.getenv('TESTER_WEB_HOOK'),
             checker=lambda x: True)

fire_bot_worker(user)
