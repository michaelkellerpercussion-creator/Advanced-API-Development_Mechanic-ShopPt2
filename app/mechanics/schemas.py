from app.extensions import ma
from app.models import Mechanic

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

from app.models import Customer

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)