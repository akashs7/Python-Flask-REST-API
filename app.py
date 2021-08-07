from flask import Flask, request
import json
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

client = MongoClient('localhost:27017')
db = client.cart
app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>API Test</h1><p>This site is a prototype API for a shopping cart<br>Use Postman to send requests</p>"

@app.route('/add_item', methods=['POST'])
def add_item():
    try:
        data = json.loads(request.data)
        item = data['item']
        amount = data['amount']
        if data and item:
            status = db.cart.insert_one({
                "item":item,
                "amount":amount,
            })
        return dumps({'message':'SUCCESS'})
    except Exception as e:
        return dumps({'error': str(e)})


@app.route('/get_items', methods = ['GET'])
def get_items():
    try:
        cart_items = db.cart.find()
        return dumps(cart_items)
    except Exception as e:
        return dumps({"error": str(e)})

@app.route('/cart_value', methods=['GET'])
def cart_value():
    try:
        cart_items = db.cart.find()
        cart_list = list(cart_items)
        amount = 0
        for each in cart_list:
            amount += each['amount']
        return dumps({"Cart value": str(amount)})
    except Exception as e:
        return dumps({"error": str(e)})
        

@app.route('/delete_item/<id>', methods =['DELETE'])
def delete_item(id):
    try:
        db.cart.delete_one({'_id': ObjectId(id)})
        return dumps({"Message":"Item deleted"})
    except Exception as e:
        return dumps({"error": str(e)})


app.run()