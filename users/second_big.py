import os

from dotenv import load_dotenv

from firebot import fire_bot_worker
from firebot.users import USERS

load_dotenv()


def is_fire_case(case):
    return '火' in str(case['案類-細項'])


def not_grass_case(case):
    return '雜草' not in str(case['案類-細項'])


def is_second_big_team_case(case):
    second_big_teams = ['水上', '民雄', '大林', '大美', '新港', '嘉太', '太保', '溪口', '雙福']
    return any(x in str(case['派遣分隊']) for x in second_big_teams)


def checker(case):
    return is_second_big_team_case(case) and not_grass_case(case) and is_fire_case(case)


user = USERS('second_big',
             os.getenv('SECONDBIG'),
             os.getenv('SECONDBIG_WEB_HOOK'),
             checker)

fire_bot_worker(user)
