from flask import Flask, request, jsonify
from models import db, Order, Zone
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/logistics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/api/orders', methods=['POST'])
def api_place_order():
    data = request.json
    # Basic validation (expand as needed)
    required_fields = [
        'customer_name', 'customer_email', 'customer_phone',
        'pickup_address', 'delivery_address', 'zone_id',
        'package_type', 'weight', 'length', 'width', 'height',
        'quantity', 'recipient_name', 'recipient_phone', 'payment_mode'
    ]
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400
    zone = Zone.query.get(data['zone_id'])
    if not zone:
        return jsonify({'success': False, 'error': 'Invalid zone'}), 400
    order = Order(
        customer_name=data['customer_name'],
        customer_email=data['customer_email'],
        customer_phone=data['customer_phone'],
        pickup_address=data['pickup_address'],
        delivery_address=data['delivery_address'],
        zone_id=data['zone_id'],
        package_type=data['package_type'],
        weight=data['weight'],
        length=data['length'],
        width=data['width'],
        height=data['height'],
        quantity=data['quantity'],
        package_description=data.get('package_description', ''),
        payment_mode=data['payment_mode'],
        recipient_name=data['recipient_name'],
        recipient_phone=data['recipient_phone'],
        estimated_delivery=datetime.utcnow()
    )
    order.total_amount = order.calculate_total_amount()
    db.session.add(order)
    db.session.commit()
    return jsonify({'success': True, 'order_id': order.id, 'reference_number': order.reference_number, 'total_amount': order.total_amount})

@app.route('/api/orders', methods=['GET'])
def api_list_orders():
    email = request.args.get('customer_email')
    if not email:
        return jsonify({'success': False, 'error': 'Missing customer_email'}), 400
    orders = Order.query.filter_by(customer_email=email).all()
    return jsonify({'success': True, 'orders': [
        {
            'id': o.id,
            'reference_number': o.reference_number,
            'recipient_name': o.recipient_name,
            'delivery_address': o.delivery_address,
            'weight': o.weight,
            'total_amount': o.total_amount,
            'status': o.delivery_status,
            'created_at': o.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for o in orders
    ]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True) 