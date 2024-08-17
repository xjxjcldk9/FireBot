import datetime

from pathlib import Path

import pandas as pd

from firebot.utils import (create_empty_record, get_df_from_website,
                           send_line_notification)


def fire_bot_worker(user):
    print(f'firebot is running {datetime.datetime.now()}')

    p = Path('.')/'record'
    p.mkdir(exist_ok=True)
    p = p / f'{user.name}_record.csv'

    if not p.exists():
        create_empty_record(p)

    df = get_df_from_website()

    if df is not None:
        record = pd.read_csv(p)
        for _, case in df.iterrows():
            send_line_notification(case, record, user)
        df.to_csv(p, index=False)
    else:
        print('webpage busy')
