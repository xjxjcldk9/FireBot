import os

from dotenv import load_dotenv

from firebot import fire_bot_worker
from firebot.users import USERS

load_dotenv()

user = USERS('tester', os.getenv('TESTER'), os.getenv('TESTER_WEB_HOOK'),
             lambda x: True)

fire_bot_worker(user)
