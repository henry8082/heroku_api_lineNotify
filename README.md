## ##基本說明

-這是一個利用python的flask 開啟LINE Front-end Framework(liff)的liff.html檔

當輸入提醒事項、日期、時間後經由ajax傳送至heroku_app.py 

所寫的flask API Endpoint post /store 並將此資料傳送至Heroku Postgres資料庫中儲存

最後在所設定的時間以Line Notifiy推播

### -使用 heroku/Flask/html/ajax/Postgres資料庫/line notify

<img src="https://github.com/henry8082/heroku_api_lineNotify/blob/master/img/S__64397333.jpg" width = "25%" /> <img src="https://github.com/henry8082/heroku_api_lineNotify/blob/master/img/events.PNG" width = "45%" /> <img src="https://github.com/henry8082/heroku_api_lineNotify/blob/master/img/S__64397335.jpg" width = "27%" />

---------------------------------------
### 重要設定：

#### heroku_app.py  - 設定Flask API、html網頁

#### clock.py - 設定排成，讓Line Notifiy推播

---------------------

HTML檔是放在templates中的liff.html

在heroku_app.py中設定endpoint 的 route為liff時 

利用render_template('liff.html')讓先建置好的HTML模板在網頁上顯示

並在Procfile中設定
<code>web: gunicorn -b :$PORT heroku_app:app --preload</code>

這一行指令分成兩個部分，其格式 <process_type>: <command> 表示：

啟用名為 web 的應用
用 gunicorn 執行 mysite.wsgi 這個模組
Gunicorn 是一個用 Python 開發的 WSGI 工具，可以用來執行 Flask 的網站。

---------------------------------------
因為在heroku上所部屬的檔案會在不使用時間超過30分鐘後自動進行休眠

並於下次重開時重置所有的資料回初始值

如果你將post上去的資料存在py檔內的list中，休眠後資料就會消失

所以使用Heroku Postgres資料庫來儲存我們所post上來的資料

並且讓Line Notifiy從資料庫抓取設定時間的資料，並推播

---------------------------------------
因推播時間為臺灣時區，跟heroku的時區不同

因此要另外在Config Vars設定下列設置

<code>TZ = Asia/Taipei</code>

---------------------------------------
最後利用apscheduler設定排程(<a href="https://github.com/maloyang/heroku-clock-howto">heroku上設定排程的參考網址</a>)

在clock.py中設定在早上8點喚醒heroku

```python
sched.add_job(wakeup, 'cron', day_of_week='mon-sun',hour=8)
```

並於每分鐘都向資料庫取資料，來判斷資料庫裡面的時間是否與當前時間相同，如相同則會推播所提醒的事項

```python
@sched.scheduled_job('cron', day_of_week='mon-sun',hour='8-23', minute='*/1')
def scheduled_job():
```

因為heroku每30分鐘就會休眠，因此設定一個wakup的排程，讓此排程每25分鐘開啟liff網頁來喚醒heroku

達到這期間不休眠的效果

```python
@sched.scheduled_job('cron', day_of_week='mon-sun',hour='8-23', minute='*/25')
def wakeup():
```



***
