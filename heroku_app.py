from flask import Flask,jsonify,request,render_template
import os
from flask_cors import CORS
import psycopg2

def insert_update(sql):
    #DATABASE_URL = os.environ['DATABASE_URL']
    DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a henry-json-server').read()[:-1]
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute(sql)
        
    conn.commit()
    cursor.close()
    conn.close()
    
def Postgres_db(sql):
    #DATABASE_URL = os.environ['DATABASE_URL']
    DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a henry-json-server').read()[:-1]
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute(sql)
    fetchall = cursor.fetchall() 
    conn.commit()
    cursor.close()
    conn.close()
    return fetchall

app = Flask(__name__)
CORS(app)
events = []

#get html
@app.route('/liff')
def get_html():
    return render_template('liff.html')

#get html
@app.route('/table')
def get_html_table():
    sql = "select * from events"
    content = Postgres_db(sql)
    content = [(str(i[0]),i[1],i[2],i[3]) for i in content]
    sqlid = {}
    for i in content:
        sqlid[str(i[0])] = True
        
    labels = ["資料庫編號","提醒事項","日期","時間"]
        
    return render_template('table.html', labels = labels, content=content,sqlid =sqlid)



#get /event
@app.route('/event')
def get_events():
    sql = "select * from events"
    content = Postgres_db(sql)
    sql2 = "SELECT column_name FROM information_schema.columns WHERE table_name = 'events'"
    labels = Postgres_db(sql2)
    labels = [l[0] for l in labels[1:]]
    for i in content:
        dic = {labels[0]:i[1],labels[1]:i[2],labels[2]:i[3]}
        events.append(dic)
    return jsonify(events)

#put  
@app.route('/table', methods=['GET','PUT'])
def put_event():
    request_data = request.get_json()

    insert_update("update events set event='{}', date='{}',time='{}' where user_id={};".format(request_data['event'],request_data['date'],request_data['time'],request_data['sqlid']))
           
    return jsonify(events)

#delete
@app.route('/table', methods=['DELETE'])
def delete_event():
    request_data = request.get_json()

    insert_update("delete from events where user_id={};".format(request_data['sqlid']))
           
    return jsonify(events)

#post /event 
@app.route('/event' , methods=['POST'])
def create_event():
    request_data = request.get_json()
    
    new_event = {
        'event':request_data['event'],
        'date':request_data['date'],
        'time':request_data['time']
    }
    insert_update("insert into events(event,date,time) values('{}','{}','{}');".format(request_data['event'],request_data['date'],request_data['time']))
    events.append(new_event)
    
    return jsonify(new_event)
    
    
app.run()
#host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 4444)) 
        