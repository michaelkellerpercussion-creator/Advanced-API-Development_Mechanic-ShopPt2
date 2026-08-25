from flask import Blueprint
from app.extensions import ma
from app.models import Inventory

inventory_bp = Blueprint('inventory_bp', __name__)

from app.inventory import routes

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)