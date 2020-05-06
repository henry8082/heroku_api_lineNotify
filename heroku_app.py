from flask import Flask,jsonify,request
import db

app = Flask(__name__)
stores = [{
    'name': "Elton's first store",
    'items': [{'name':'my item 1', 'price': 30 }],
    },
    {
    'name': "Elton's second store",
    'items': [{'name':'my item 2', 'price': 15 }],
    },
]
#get /store
@app.route('/store')
def get_stores():
    return jsonify(stores)
@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
        return jsonify ({'message': 'store not found'})
#get /store/<name>/item data: {name :}
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify( {'items':store['items'] } )
    return jsonify ({'message':'store not found'})
#post /store data: {name :}
@app.route('/store' , methods=['POST'])
def create_event():
    request_data = request.get_json()
    new_store = {
        'event':request_data['event'],
        'date':request_data['date'],
        'time':request_data['time']
    }
    db.insert(request_data['event'],request_data['date'],request_data['time'])
    stores.append(new_store)
    
    return jsonify(new_store)
#post /store/<name> data: {name :}
@app.route('/store/<string:name>/item' , methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
        store['items'].append(new_item)
        return jsonify(new_item)
    
app.run()