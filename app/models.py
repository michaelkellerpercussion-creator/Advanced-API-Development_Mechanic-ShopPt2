from app.extensions import db

# JUNCTION TABLE: Service Tickets / Mechanics
service_mechanics = db.Table(
    'service_mechanics',
    db.Column('ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'), primary_key=True)
)

# JUNCTION ABLE: Service Tickets / Inventory Parts
ticket_inventory = db.Table(
    'ticket_inventory',
    db.Column('ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('inventory_id', db.Integer, db.ForeignKey('inventory.id'), primary_key=True)
)


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    tickets = db.relationship('ServiceTicket', backref='customer', lazy=True)


class Mechanic(db.Model):
    __tablename__ = 'mechanics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    salary = db.Column(db.Float, nullable=False)


class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)


class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'

    id = db.Column(db.Integer, primary_key=True)
    vin = db.Column(db.String(17), nullable=False)
    service_desc = db.Column(db.String(255), nullable=False)
    #Foreign Key to customers
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    mechanics = db.relationship(
        'Mechanic',
        secondary=service_mechanics,
        backref=db.backref('service_tickets', lazy='dynamic')
    )

    parts = db.relationship(
        'Inventory',
        secondary=ticket_inventory,
        backref=db.backref('service_tickets', lazy='dynamic')
    )