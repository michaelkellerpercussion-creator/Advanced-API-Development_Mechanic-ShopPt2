from flask import request, jsonify
from app.customers import customers_bp
from app.customers.schemas import customer_schema, customers_schema
from app.models import Customer
from app.extensions import db

@customers_bp.route('/', methods=['POST'])
def create_customer():
    data = request.get_json()
    errors = customer_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_customer = customer_schema.load(data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

@customers_bp.route('/', methods=['GET'])
def get_customers():
    customers = db.session.query(Customer).all()
    return customers_schema.jsonify(customers), 200

@customers_bp.route('/<int:id>', methods=['GET'])
def get_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    return customer_schema.jsonify(customer), 200

@customers_bp.route('/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404

    data = request.get_json()
    errors = customer_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    for key, value in data.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200

@customers_bp.route('/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer {id} successfully deleted"}), 200