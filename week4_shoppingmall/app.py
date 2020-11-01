from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/')
def homework():
    return render_template('index.html')


@app.route('/order', methods=['POST'])
def make_order():
    name = request.form['name']
    qty = request.form['qty']
    address = request.form['address']
    phone = request.form['phone']

    print(name, qty, address, phone)

    doc = {
        'name': name,
        'qty': qty,
        'address': address,
        'phone': phone
    }

    db.orders.insert_one(doc)

    return jsonify({'result': 'success'})


@app.route('/order', methods=['GET'])
def view_orders():
    orders = list(db.orders.find({}, {'_id': 0}))
    print(orders)
    return jsonify({'result': 'success', 'orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
