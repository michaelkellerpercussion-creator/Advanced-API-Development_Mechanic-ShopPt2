from flask import Flask
from app.extensions import cache, db, limiter, ma


def create_app(config_name="DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(f"app.config.{config_name}")

    from app.customers import customers_bp
    from app.inventory import inventory_bp
    from app.mechanics import mechanics_bp
    from app.service_tickets import service_tickets_bp

    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")

    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)

    return app
