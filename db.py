import os
import psycopg2
from flask import Flask,jsonify,request

def insert(event,date,time):
    DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a henry-json-server').read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute("inser into events(event,date,time) values({},{},{})".format(event,date,time))
        
    conn.commit()
    cursor.close()
    conn.close()




"""
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
"""



