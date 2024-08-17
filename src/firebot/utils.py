import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


def send_payload(payload, token):
    data = {'message': payload}
    response = requests.post('https://notify-api.line.me/api/notify',
                             headers={'Authorization': f'Bearer {token}'},
                             data=data)
    return response


def get_df_from_website():
    try:
        df = pd.read_html(os.getenv("WEBSITE"))[0]
    except:
        df = None
    return df


def send_line_notification(case, record, user):
    highlight = '🚑'*5

    if '火' in case['案類-細項']:
        highlight = '🚒'*5

    case_num = case['受理時間'].split()[1].replace(':', '')

    payload = f"\n{highlight}\n編號：{case_num}\n地點：{case['案發地點']}\n類型：{case['案類-細項']}\n派遣：{case['派遣分隊']}\n狀態：{case['案件狀態']}"

    seen_changed = False
    unseen = False

    # check if this case has sent
    seen_case = record[record['受理時間'] == case['受理時間']]

    if len(seen_case) > 0:
        # 檢查是否發生改變
        if not (seen_case.iloc[0] == case).all():
            seen_changed = True
    else:
        unseen = True

    if (user.check(case)) and (seen_changed or unseen):
        send_payload(payload, user.token)


def create_empty_record(path):
    df = pd.DataFrame(columns=["受理時間", "案類-細項", "案發地點", "派遣分隊", "案件狀態"])
    df.to_csv(path)
