from flask import request, jsonify
from app.mechanics import mechanics_bp
from app.mechanics.schemas import mechanic_schema, mechanics_schema
from app.models import Mechanic
from app.extensions import db

@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    data = request.get_json()
    errors = mechanic_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    new_mechanic = mechanic_schema.load(data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    mechanics = db.session.query(Mechanic).all()
    return mechanics_schema.jsonify(mechanics), 200

@mechanics_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404

    data = request.get_json()
    errors = mechanic_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    for key, value in data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

@mechanics_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {id} successfully deleted"}), 200