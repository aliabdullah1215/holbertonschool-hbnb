from flask import Blueprint
from flask_restx import Api

from app.api.v1.status import status_ns
from app.api.v1.users import users_ns
from app.api.v1.places import places_ns
from app.api.v1.reviews import reviews_ns
from app.api.v1.amenities import amenities_ns

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")
api = Api(api_v1_bp)

api.add_namespace(status_ns)
api.add_namespace(users_ns)
api.add_namespace(places_ns)
api.add_namespace(reviews_ns)
api.add_namespace(amenities_ns)
