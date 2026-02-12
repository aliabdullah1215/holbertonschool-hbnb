from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

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
    def post(self):
        """Protected: Create a new place"""
        current_user_id = get_jwt_identity()
        data = api.payload

        if data['price'] <= 0:
            return {'error': 'Price must be a positive number'}, 400
        if not (-90 <= data['latitude'] <= 90):
            return {'error': 'Latitude must be between -90 and 90'}, 400
        if not (-180 <= data['longitude'] <= 180):
            return {'error': 'Longitude must be between -180 and 180'}, 400

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

        # --- تعديل: جلب اسم المضيف الحقيقي ---
        host = facade.get_user(place.owner_id)
        host_name = f"{host.first_name} {host.last_name}" if host else "Owner"

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'host_name': host_name, # إرسال اسم المضيف للواجهة
            'owner_id': place.owner_id,
            # إرسال المرافق بشكل منظم
            'amenities': [{'id': a.id, 'name': a.name} for a in place.amenities],
            # --- تعديل: إرسال التقييمات مع أسماء أصحابها ---
            'reviews': [
                {
                    'id': r.id, 
                    'text': r.text, 
                    'rating': r.rating,
                    # جلب الاسم الكامل من كائن المستخدم المرتبط بالتقييم
                    'user_name': f"{r.user.first_name} {r.user.last_name}" if hasattr(r, 'user') and r.user else "Anonymous User"
                } for r in place.reviews
            ]
        }, 200

    @jwt_required()
    def put(self, place_id):
        """Protected: Update place details"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        data = api.payload
        updated_place = facade.update_place(place_id, data)
        return {'id': updated_place.id, 'message': 'Place updated successfully'}, 200

@api.route('/<place_id>/amenities/<amenity_id>')
class PlaceAmenityResource(Resource):
    @jwt_required()
    @api.response(200, 'Amenity added to place successfully')
    @api.response(404, 'Place or Amenity not found')
    def post(self, place_id, amenity_id):
        """Link an amenity to a place (Owner or Admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        if not is_admin and place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        facade.add_amenity_to_place(place_id, amenity_id)
        return {'message': 'Amenity added to place successfully'}, 200
    