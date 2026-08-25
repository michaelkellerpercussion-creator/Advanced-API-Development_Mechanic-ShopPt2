from flask import request, jsonify
from sqlalchemy import func
from app.mechanics import mechanics_bp
from app.mechanics.schemas import mechanic_schema, mechanics_schema
from app.models import Mechanic, service_mechanics
from app.extensions import db

#sort by most active
@mechanics_bp.route('/most-active', methods=['GET'])
def get_most_active_mechanics():
    results = db.session.query(
        Mechanic, func.count(service_mechanics.c.ticket_id).label('ticket_count')
    ).outerjoin(
        service_mechanics, Mechanic.id == service_mechanics.c.mechanic_id
    ).group_by(Mechanic.id).order_by(func.count(service_mechanics.c.ticket_id).desc()).all()

    output = []
    for mechanic, count in results:
        userdata = mechanic_schema.dump(mechanic)
        userdata['tickets_worked'] = count
        output.append(userdata)

    return jsonify(output), 200

@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    userdata = request.get_json()
    errors = mechanic_schema.validate(userdata)
    if errors:
        return jsonify(errors), 400
    
    new_mechanic = mechanic_schema.load(userdata)
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

    userdata = request.get_json()
    for key, value in userdata.items():
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
    return jsonify({"message": f"Mechanic {id} deleted"}), 200