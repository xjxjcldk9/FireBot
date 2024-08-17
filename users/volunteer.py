import os

from dotenv import load_dotenv

from firebot import fire_bot_worker
from firebot.users import USERS

load_dotenv()


def is_water(case):
    return '水上' in case['派遣分隊']


def is_fire_case(case):
    return '火' in case['案類-細項']


def not_grass_case(case):
    return '雜草' not in case['案類-細項']


def checker(case):
    return is_water(case) and not_grass_case(case) and is_fire_case(case)


user = USERS('volunteer',
             os.getenv('VOLUNTEER'),
             checker)

fire_bot_worker(user)
