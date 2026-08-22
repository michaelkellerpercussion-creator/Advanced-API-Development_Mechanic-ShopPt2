from flask import Blueprint

customers_bp = Blueprint('customers_bp', __name__)

from app.customers import routes