from flask import Flask
from app.extensions import db, ma
from app.customers import customers_bp
from app.mechanics import mechanics_bp
from app.service_tickets import service_tickets_bp
from app.customers import routes

def create_app(config_class="app.config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)

    # Register Blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')  
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service-tickets')

    return app