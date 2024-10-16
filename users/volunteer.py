import os

from dotenv import load_dotenv

from firebot import fire_bot_worker
from firebot.users import USERS

load_dotenv()


def is_water(case):
    return '水上' in str(case['派遣分隊'])


def is_fire_case(case):
    return '火' in str(case['案類-細項'])



def checker(case):
    return is_water(case) and is_fire_case(case)


user = USERS('volunteer',
             os.getenv('VOLUNTEER'),
             os.getenv('VOLUNTEER_WEB_HOOK'),
             checker)

fire_bot_worker(user)
