from app.extensions import db

#Many-to-Many Relationship between Service Tickets and Mechanics
service_mechanics = db.Table(
    'service_mechanics',
    db.Column('ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'), primary_key=True)
)


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    # ONe-to-Many relationship with ServiceTicket
    tickets = db.relationship('ServiceTicket', backref='customer', lazy=True)

    def __repr__(self):
        return f"<Customer {self.name}>"


class Mechanic(db.Model):
    __tablename__ = 'mechanics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    salary = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Mechanic {self.name}>"


class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'

    id = db.Column(db.Integer, primary_key=True)
    vin = db.Column(db.String(17), nullable=False)
    service_desc = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    # Many-to-MAny relationship with Mechanic
    mechanics = db.relationship(
        'Mechanic',
        secondary=service_mechanics,
        backref=db.backref('service_tickets', lazy='dynamic')
    )

    def __repr__(self):
        return f"<ServiceTicket {self.id} - VIN: {self.vin}>"