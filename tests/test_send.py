from firebot.send import get_df_from_website


def test_fetch_df():
    df = get_df_from_website()
    if df:
        assert set(df.columns) == ['受理時間', '案類-細項', '案發地點', '派遣分隊', '案件狀態']
