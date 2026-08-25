from flask import request, jsonify
from app.inventory import inventory_bp
from app.inventory.schemas import inventory_schema, inventories_schema
from app.models import Inventory
from app.extensions import db

@inventory_bp.route('/', methods=['POST'])
def create_part():
    userdata = request.get_json()
    errors = inventory_schema.validate(userdata)
    if errors:
        return jsonify(errors), 400

    new_part = inventory_schema.load(userdata)
    db.session.add(new_part)
    db.session.commit()
    return inventory_schema.jsonify(new_part), 201

@inventory_bp.route('/', methods=['GET'])
def get_parts():
    parts = db.session.query(Inventory).all()
    return inventories_schema.jsonify(parts), 200

@inventory_bp.route('/<int:id>', methods=['PUT'])
def update_part(id):
    part = db.session.get(Inventory, id)
    if not part:
        return jsonify({"message": "Part not found"}), 404

    userdata = request.get_json()
    for key, value in userdata.items():
        setattr(part, key, value)

    db.session.commit()
    return inventory_schema.jsonify(part), 200

@inventory_bp.route('/<int:id>', methods=['DELETE'])
def delete_part(id):
    part = db.session.get(Inventory, id)
    if not part:
        return jsonify({"message": "Part not found"}), 404

    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f"Part {id} deleted"}), 200