from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Amenity name')
})


def admin_required():
    claims = get_jwt()
    return claims.get('is_admin', False)


@api.route('/')
class AmenityList(Resource):

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    def post(self):
        """Admin only: Create a new amenity"""
        if not admin_required():
            return {'error': 'Admin privileges required'}, 403

        data = api.payload
        amenity = facade.create_amenity(data['name'])

        return {
            'id': amenity.id,
            'name': amenity.name
        }, 201


@api.route('/<amenity_id>')
class AmenityResource(Resource):

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    def put(self, amenity_id):
        """Admin only: Update an amenity"""
        if not admin_required():
            return {'error': 'Admin privileges required'}, 403

        amenity = facade.update_amenity(amenity_id, api.payload)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200
