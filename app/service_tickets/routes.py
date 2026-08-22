from flask import request, jsonify
from app.service_tickets import service_tickets_bp
from app.service_tickets.schemas import service_ticket_schema, service_tickets_schema
from app.models import ServiceTicket, Mechanic
from app.extensions import db

@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    data = request.get_json()
    errors = service_ticket_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_ticket = service_ticket_schema.load(data)
    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket), 201

@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    tickets = db.session.query(ServiceTicket).all()
    return service_tickets_schema.jsonify(tickets), 200

@service_tickets_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket or not mechanic:
        return jsonify({"message": "Service Ticket or Mechanic not found"}), 404

    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()

    return service_ticket_schema.jsonify(ticket), 200

@service_tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket or not mechanic:
        return jsonify({"message": "Service Ticket or Mechanic not found"}), 404

    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()

    return service_ticket_schema.jsonify(ticket), 200