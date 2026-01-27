from flask_restx import Api

from app.api.v1.users import api as users_api
from app.api.v1.auth import api as auth_api
from app.api.v1.protected import api as protected_api
from app.api.v1.places import api as places_api

api = Api(
    title='HBnB API',
    version='1.0',
    description='HBnB REST API'
)

api.add_namespace(users_api, path='/api/v1/users')
api.add_namespace(auth_api, path='/api/v1/auth')
api.add_namespace(protected_api, path='/api/v1/protected')
api.add_namespace(places_api, path='/api/v1/places')
