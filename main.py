from flask import Flask, jsonify, request
import datetime

app = Flask(__name__)

# Sample data for lightning deals
lightning_deals = [
    {
        'id': 1,
        'product_name': 'Product A',
        'actual_price': 100.0,
        'final_price': 80.0,
        'total_units': 10,
        'available_units': 5,
        'expiry_time': datetime.datetime.utcnow() + datetime.timedelta(hours=6)
    },
    {
        'id': 2,
        'product_name': 'Product B',
        'actual_price': 200.0,
        'final_price': 150.0,
        'total_units': 20,
        'available_units': 10,
        'expiry_time': datetime.datetime.utcnow() + datetime.timedelta(hours=10)
    }
]

# for accessing available unexpired deals
@app.route('/deals', methods=['GET'])
def get_deals():
    current_time = datetime.datetime.utcnow()
    available_deals = []
    for deal in lightning_deals:
        if current_time < deal['expiry_time'] and deal['available_units'] > 0:
            available_deals.append(deal)
    return jsonify({'deals': available_deals})

# for placing an order for a deal
@app.route('/order', methods=['POST'])
def place_order():
    data = request.get_json()
    deal_id = data['deal_id']
    units = data['units']
    for deal in lightning_deals:
        if deal['id'] == deal_id:
            if deal['available_units'] >= units and datetime.datetime.utcnow() < deal['expiry_time']:
                deal['available_units'] -= units
                return jsonify({'message': 'Order placed successfully'})
            else:
                return jsonify({'message': 'Deal expired or not enough units available'})
    return jsonify({'message': 'Deal not found'})

#  for checking order status
@app.route('/order/<int:order_id>', methods=['GET'])
def get_order_status(order_id):
    # Code to check order status using order_id
    return jsonify({'status': 'Delivered'})

if __name__ == '__main__':
    app.run(debug=True,port=8000)
