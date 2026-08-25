from marshmallow import fields
from app.extensions import ma
from app.models import Customer

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    # Explicitly define password field to ensure load_instance works smoothly
    password = fields.String(required=True, load_only=True)

    class Meta:
        model = Customer
        load_instance = True

class LoginSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        fields = ("email", "password")

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = LoginSchema()