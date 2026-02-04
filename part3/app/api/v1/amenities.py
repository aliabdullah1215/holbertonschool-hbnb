from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

# تعريف نموذج البيانات للمرافق
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity (e.g., WiFi, Pool)')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Create a new amenity (Admin only)"""
        # التحقق من صلاحيات الأدمن
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = api.payload
        amenity = facade.create_amenity(data)
        return {'id': amenity.id, 'name': amenity.name}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Get all amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': a.id, 'name': a.name} for a in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information (Admin only)"""
        # التحقق من صلاحيات الأدمن
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, data)
        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404
        return {'message': 'Amenity updated successfully'}, 200
