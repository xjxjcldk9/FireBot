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

    payload = f"\n{highlight}\
    \n時間：{case['受理時間']}\
    \n地點：{case['案發地點']}\
    \n類型：{case['案類-細項']}\
    \n派遣：{case['派遣分隊']}\
    \n狀態：{case['案件狀態']}"

    seen_changed = False
    unseen = False

    # check if this case has sent
    seen_cases = record[record['受理時間'] == case['受理時間']]

    if len(seen_cases) > 0:
        # 檢查是否發生改變
        seen_case = seen_cases.iloc[0]

        # 都先fillna，因為nan會不相等
        seen_case = seen_case.fillna(1)
        case = case.fillna(1)
        if not (seen_case == case).all():
            seen_changed = True
    else:
        unseen = True

    if (user.check(case)) and (seen_changed or unseen):
        send_payload(payload, user.token)


def create_empty_record(path):
    df = pd.DataFrame(columns=["受理時間", "案類-細項", "案發地點", "派遣分隊", "案件狀態"])
    df.to_csv(path)
