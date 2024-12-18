import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from firebot import fire_bot_worker
from firebot.users import USERS
from firebot.utils import (create_empty_record, get_df_from_website,
                           send_line_notification, send_payload)

load_dotenv()

user = USERS('tester', os.getenv('TESTER'), lambda x: True)

p = Path('.') / 'record'
p.mkdir(exist_ok=True)


def test_fetch_df():
    df = get_df_from_website()
    if df is not None:
        df.to_csv(p / 't_record.csv', index=False)
        assert set(df.columns) == set(
            ['受理時間', '案類-細項', '案發地點', '派遣分隊', '案件狀態'])
        for _, case in df.iterrows():
            assert isinstance(case['派遣分隊'], str)


def test_empty_record():
    create_empty_record(p / 'empty.csv')


def test_send_payload():
    response = send_payload('測試測試', os.getenv('TESTER'))
    assert response.status_code == 200


def test_send_line_notification():
    record = pd.read_csv(p / 't_record.csv')
    df = get_df_from_website()
    for _, case in df.iterrows():
        send_line_notification(case, record, user)
