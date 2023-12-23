import requests
import pandas as pd
import os
from datetime import datetime
import sys


os.chdir('D:\\Users\\cycfb206\\Desktop\\LineBot')




website = 'http://cycfb.cyhg.gov.tw/DisasterPrevent.aspx?n=5F10482409025004&sms=ED4E0CDDC2EA92E6'
token = 'vrB9tyzVyRyXVPQGahZzPJOUmzDf75a8k9wre42xTDn'
fire_token = 'znybPQWIrKYZ6G6638Vp1aub56nEc7vuoKk2jDA1sYC'


test = '4uHj0MLcvQeC7oqmWKJpy1mSurFEioMmjs4njUzZDmz'




try:
    df = pd.read_html(website)[0]
except:
    payload = {'message': '網頁忙碌中!'}
    r = requests.post('https://notify-api.line.me/api/notify',
                  headers={'Authorization': 'Bearer {}'.format(test)}, params=payload)
    sys.exit(1)
    

cases = df[(df['派遣分隊'].str.contains('水上分隊'))]



#讀取紀錄，若記錄檔不存在，則創造新的
if not os.path.exists('record.csv'):
    template = pd.DataFrame(columns=[*cases.columns, '創造時間'])
    template.to_csv('record.csv', index=False)




#測試有在跑

t = datetime.now().strftime("%H:%M:%S")
payload = {'message': f'機器人工作中。現在時間{t}',
           'notificationDisabled': True}
r = requests.post('https://notify-api.line.me/api/notify',
                  headers={'Authorization': 'Bearer {}'.format(test)}, params=payload)




def detectChange(row, recordRow):
    detectedCols = [1,2,4]
    for col in detectedCols:
        if row.iloc[col] != recordRow.iloc[col]:
            return True
    return False


def sendLine(row):
    highlight = '⚠️'*5

    is_fire = False

    if '救護' in row['案類-細項']:
        highlight = '🚑'*5
    elif '火' in row['案類-細項']:
        highlight = '🚒'*5
        is_fire = True
    
    payload = {'message': '\n{}\n地點：{}\n類型：{}\n狀態：{}'.format(
        highlight,
        row['案發地點'].split()[1],
        row['案類-細項'].split()[1],
        row['案件狀態'].split()[1]
    )}
    
    #一般
    requests.post('https://notify-api.line.me/api/notify',
                  headers={'Authorization': 'Bearer {}'.format(token)}, params=payload)
    
    #火警
    if is_fire:
        requests.post('https://notify-api.line.me/api/notify',
                  headers={'Authorization': 'Bearer {}'.format(fire_token)}, params=payload)



dt_format = "%Y/%m/%d %H:%M:%S"


def killRecord(record):
    for index in record.index:
        if (datetime.now() - datetime.strptime(record['創造時間'].loc[index],  dt_format)).days > 1:
            record = record.drop(index)

    record.to_csv('record.csv', index=False)




#實際執行

record = pd.read_csv('record.csv')

for index, row in cases.iterrows():
    row['創造時間'] = datetime.now().strftime(dt_format)
    tmpDf = pd.DataFrame(row).T
    if (record['受理時間'].str.contains(row['受理時間']).any()):
        recordRow = record[record['受理時間'] == row['受理時間']].iloc[0]
        id = recordRow.name
        if (detectChange(row, recordRow)):
            record = record.drop(id)
            record = pd.concat([record, tmpDf])
            record.to_csv('record.csv', index = False)
            sendLine(row)
    elif('任務完成' not in row['案件狀態']):
        record = pd.concat([record, tmpDf])
        record.to_csv('record.csv', index=False)
        sendLine(row)
        
killRecord(record)