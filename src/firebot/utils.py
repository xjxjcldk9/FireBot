import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


def send_payload(payload, token):
    requests.post('https://notify-api.line.me/api/notify',
                  headers={'Authorization': f'Bearer {token}'},
                  params=payload)


def get_df_from_website():
    try:
        df = pd.read_html(os.getenv("WEBSITE"))[0]
    except:
        df = None
    return df


def is_water_main_case(case):
    return '水上' in case['派遣分隊']


def is_fire_case(case):
    return '火' in case['案類-細項']


def not_grass_case(case):
    return '雜草' not in case['案類-細項']


def is_second_big_team_case(case):
    second_big_teams = ['水上', '民雄', '大林', '大美', '新港', '嘉太', '太保', '溪口', '雙福']
    return any(x in case['派遣分隊'] for x in second_big_teams)


def has_status_changes(seen_row, case):
    status_col = ['案類-細項', '案發地點', '派遣分隊', '案件狀態']
    any_change = (seen_row[status_col] != case[status_col]).any()
    case_not_na = len(case['案件狀態'].split()) > 1
    return any_change and case_not_na


def decide_recipient_for_message(case, record):
    recipient_dict = {"volunteerFire": False,
                      "secondBigTeam": False,
                      "waterMain": False}

    seen_record = record[record['受理時間'] == case['受理時間']]
    if len(seen_record) != 0:
        seen_row = seen_record.iloc[0]
        if (is_water_main_case(case) and
                has_status_changes(seen_row, case)):
            recipient_dict['waterMain'] = True
            if is_fire_case(case):
                recipient_dict['volunteerFire'] = True
        if (is_second_big_team_case(case) and
                has_status_changes(seen_row, case)):

            if (is_fire_case(case) and not_grass_case(case)):
                recipient_dict['secondBigTeam'] = True
    else:
        if '任務完成' not in case['案件狀態']:
            if is_water_main_case(case):
                recipient_dict['waterMain'] = True
                if is_fire_case(case):
                    recipient_dict['volunteerFire'] = True
            if (is_second_big_team_case(case) and
                    is_fire_case(case) and
                    not_grass_case(case)):
                recipient_dict['secondBigTeam'] = True

    return recipient_dict


def send_line_notification(case, record, test=False, to_who=...):
    highlight = '🚑'*5

    if '火' in case['案類-細項']:
        highlight = '🚒'*5

    case_num = case['受理時間'].split()[1].replace(':', '')

    payload = {'message':
               f'''
               \n{highlight}
               \n編號：{case_num}
               \n地點：{case['案發地點']}
               \n類型：{case['案類-細項']}
               \n派遣：{case['派遣分隊']}
               \n狀態：{case['案件狀態']}
               '''}

    send = False
    if to_who.check(case):

        # check if this case has sent
        if case['受理時間'] in record['受理時間']:
            # 檢查是否發生改變
            seen_case = record[record['受理時間'] == case['受理時間']].iloc[0]
            if not (seen_case == case).all():
                send = True
        elif '任務完成' not in case['案件狀態']:
            send = True

    if send:
        send_payload(payload, to_who.token)


def create_empty_record(path):
    df = pd.DataFrame(columns=["受理時間", "案類-細項", "案發地點", "派遣分隊", "案件狀態"])
    df.to_csv(path)
