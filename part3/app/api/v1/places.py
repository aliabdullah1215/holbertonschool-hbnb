from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

# نموذج طلب البيانات مع إضافة قيود منطقية
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude (-90 to 90)'),
    'longitude': fields.Float(required=True, description='Longitude (-180 to 180)')
})

@api.route('/')
class PlaceList(Resource):
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Public: Get list of all places"""
        places = facade.get_all_places()
        return [
            {
                'id': p.id,
                'title': p.title,
                'price': p.price
            } for p in places
        ], 200

    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place created successfully')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Protected: Create a new place (Authenticated users only)"""
        current_user_id = get_jwt_identity()
        data = api.payload

        # قيود إضافية قبل الإرسال للـ Facade
        if data['price'] <= 0:
            return {'error': 'Price must be a positive number'}, 400
        if not (-90 <= data['latitude'] <= 90):
            return {'error': 'Latitude must be between -90 and 90'}, 400
        if not (-180 <= data['longitude'] <= 180):
            return {'error': 'Longitude must be between -180 and 180'}, 400

        # ربط الهوية من التوكن آلياً لضمان الأمان
        data['owner_id'] = current_user_id

        try:
            place = facade.create_place(data)
            return {
                'id': place.id,
                'title': place.title,
                'owner_id': place.owner_id,
                'message': 'Place created successfully'
            }, 201
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Public: Get detailed information about a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner_id
        }, 200

    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """Protected: Update place details (Owner or Admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # التحقق من الصلاحية: المالك الحقيقي أو المسؤول (Admin)
        if not is_admin and place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        # التحقق من منطق البيانات المرسلة في التحديث
        data = api.payload
        if 'price' in data and data['price'] <= 0:
            return {'error': 'Price must be a positive number'}, 400

        updated_place = facade.update_place(place_id, data)
        return {
            'id': updated_place.id,
            'message': 'Place updated successfully'
        }, 200

    @jwt_required()
    @api.response(204, 'Place deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Protected: Delete a place (Owner or Admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200
