from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

db = SQLAlchemy()
ma = Marshmallow()
# 200 per day/50 per hour limit
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

# stores data for faster queries
cache = Cache(config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})