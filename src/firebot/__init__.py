from pathlib import Path

import pandas as pd

from firebot.utils import (create_empty_record, get_df_from_website,
                           send_line_notification)


def main():
    p = Path('.')/'record'
    p.mkdir(exist_ok=True)
    p = p / 'record.csv'

    if not p.exists():
        create_empty_record(p)

    df = get_df_from_website()

    if df is not None:
        record = pd.read_csv(p)
        for _, case in df.iterrows():
            send_line_notification(case, record)
        df.to_csv(p, index=False)
    else:
        print('webpage busy')


if __name__ == '__main__':
    main()
