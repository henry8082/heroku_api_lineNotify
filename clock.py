import os
import psycopg2
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import requests
from datetime import timedelta


def pushevent(event,temp):
    token = '0HU2KZzhUDD3pZ2rz2RfEKsMOg1iCQhuo2b6OTdUjgN'#提醒專區的token
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'Authorization': f'Bearer {token}'
    } 
    payload = {
     'message':'\n\n提醒項目：\n{}\n\n提醒時間：\n{}\n\nliff網址：\nhttps://liff.line.me/1654185844-JDk62Nww'.format(event,temp),
    }

    res = requests.post('https://notify-api.line.me/api/notify', data = payload, headers = headers)    

sched = BlockingScheduler()


def delete_id(Id):
    #DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a henry-json-server').read()[:-1]
    DATABASE_URL = os.environ['DATABASE_URL']
    
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM events WHERE user_id = {};".format(Id))
        
    conn.commit()
    cursor.close()
    conn.close()    



#@sched.scheduled_job('cron', day_of_week='mon-sun',hour='8-23', minute='*/1')
def scheduled_job():
    now = datetime.datetime.now()
    print(now)
    
    #DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a henry-json-server').read()[:-1]
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * from events")
        
    conn.commit()
    
    data = []
    while True:
        temp = cursor.fetchone()
        if temp:
            data.append(temp)
        else:
            break
    #print(data)

    cursor.close()
    conn.close()

    s_time = datetime.datetime.strptime(str((datetime.datetime.now() + timedelta(days=1)).date())+' 0:00', '%Y-%m-%d %H:%M')
    e_time =  datetime.datetime.strptime(str((datetime.datetime.now() + timedelta(days=1)).date())+' 8:00', '%Y-%m-%d %H:%M')
    for i in data:
        temp = i[2]+" "+i[3]    
        temp_datetime = datetime.datetime.strptime(temp, "%Y-%m-%d %H:%M") #將字串轉為datetime
        if i[2]==now.strftime("%Y-%m-%d"):
            if (temp_datetime - now).total_seconds()//60 <=0:
                pushevent(i[1],temp)
                delete_id(i[0])
            elif(temp_datetime > s_time and temp_datetime < e_time and now >= s_time):
                pushevent(i[1],temp)
                delete_id(i[0])     
                
@sched.scheduled_job('cron', day_of_week='mon-sun',hour='8-23', minute='*/25')
def wakeup():
    url = "https://henry-json-server.herokuapp.com/liff"
    requests.get(url)
    now = datetime.datetime.now()
    print(now)
    


sched.add_job(scheduled_job, 'cron', day_of_week='mon-sun',hour='8-23', minute='*/1')
sched.start()


"""
def insert(event,date,time):
    DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a henry-json-server').read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute("inser into events(event,date,time) values({},{},{})".format(event,date,time))
        
    conn.commit()
    cursor.close()
    conn.close()


DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a henry-json-server').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'account'")
    
conn.commit()

data = []
while True:
    temp = cursor.fetchone()
    if temp:
        data.append(temp)
    else:
        break
print(data)

cursor.close()
conn.close()



import datetime
 
# 范围时间
s_time = datetime.datetime.strptime(str((datetime.datetime.now() + timedelta(days=1)).date())+' 0:00', '%Y-%m-%d %H:%M')
e_time =  datetime.datetime.strptime(str((datetime.datetime.now() + timedelta(days=1)).date())+' 8:00', '%Y-%m-%d %H:%M')
 
# 当前时间
n_time = datetime.datetime.now()
aaa = datetime.datetime.strptime("2020/5/9 11:40", "%Y-%m-%d %H:%M")
 
# 判断当前时间是否在范围时间内
if (aaa > s_time and aaa < e_time) and (n_time >= s_time):
    print("不在時間內")
else: print(n_time)
"""