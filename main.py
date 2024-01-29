import requests
import pandas as pd
import os
from datetime import datetime
import sys
import json


with open('website.txt') as f:
    website = f.readline()

with open('tokens.json') as f:
    tokens = json.load(f)


def send_payload(payload, token):
    requests.post('https://notify-api.line.me/api/notify',
                  headers={'Authorization': f'Bearer {token}'},
                  params=payload)


def get_dataframe_from_website():
    try:
        df = pd.read_html(website)[0]
    except:
        payload = {'message': '網頁忙碌中!'}
        send_payload(payload, tokens['testing'])
        sys.exit(1)
    return df


def test_if_running():
    # 測試有在跑
    t = datetime.now().strftime("%H:%M:%S")
    payload = {'message': f'機器人工作中。現在時間{t}',
               'notificationDisabled': True}
    send_payload(payload, tokens['testing'])


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


def send_line_notification(case, record):
    highlight = '🚑'*5

    if '火' in case['案類-細項']:
        highlight = '🚒'*5

    case_splitted = case.str.split()
    case_num = case_splitted.str[2]['受理時間'].replace(':', '')

    payload = {'message': '\n{}\n編號：{}\n地點：{}\n類型：{}\n派遣：{}\n狀態：{}'.format(
        highlight,
        case_num,
        case_splitted.str[1]['案發地點'],
        case_splitted.str[1]['案類-細項'],
        case_splitted.str[1]['派遣分隊'],
        case_splitted.str[1]['案件狀態']
    )}

    recipient_dict = decide_recipient_for_message(case, record)

    for place, send in recipient_dict.items():
        if send:
            send_payload(payload, tokens[place])


# 實際執行

def main():
    test_if_running()
    df = get_dataframe_from_website()
    record = pd.read_csv('record.csv')
    for _, case in df.iterrows():
        send_line_notification(case, record)
    df.to_csv('record.csv', index=False)


main()
