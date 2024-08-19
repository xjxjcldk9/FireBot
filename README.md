# FireBot

即時災害通報機器人

會自動爬取嘉義縣消防災害網站  
並根據設定條件選擇要傳送的案件狀態

# Requirements

- python3
- Line Notification API KEY

# Install

```shell
pip install .
```

# 如何使用

在```users/```資料夾中新增使用者，設定好想要傳送的條件

目前的案件傳送條件是：

- 使用者設定條件
- 沒看過的案件
- 看過但是狀態改變

# 如何部署

進入虛擬環境並且資料夾位於```users/```當中

```shell
while true; do 檔名.py; sleep 60; done
```

系統就會每60秒偵測一次，並把錯誤都output出來
