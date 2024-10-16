import os

from dotenv import load_dotenv

from firebot import fire_bot_worker
from firebot.users import USERS

load_dotenv()


def checker(case):
    return '水上' in str(case['派遣分隊'])


user = USERS('water_main',
             os.getenv('WATERMAIN'),
             os.getenv('WATERMAIN_WEB_HOOK'),
             checker)

fire_bot_worker(user)
