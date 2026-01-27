from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Models for related entities (for docs)
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'review': fields.List(fields.Nested(review_model), description='List of reviews')
})


def place_to_dict(place):
    """Serialize place including owner and amenities."""
    owner = place.owner
    owner_dict = {
        'id': owner.id,
        'first_name': owner.first_name,
        'last_name': owner.last_name,
        'email': owner.email
    } if owner else None

    amenities = [{'id': a.id, 'name': a.name} for a in getattr(place, 'amenities', [])]
    reviews = [{
        'id': r.id,
        'text': r.text,
        'rating': r.rating,
        'user_id': r.user.id if getattr(r, 'user', None) else None
    } for r in getattr(place, 'reviews', [])]


    return {
        'id': place.id,
        'title': place.title,
        'description': place.description,
        'price': place.price,
        'latitude': place.latitude,
        'longitude': place.longitude,
        'owner': owner_dict,
        'amenities': amenities,
        'created_at': place.created_at.isoformat() if hasattr(place, 'created_at') else None,
        'update_at': place.updated_at.isoformat() if hasattr(place, 'updated_at') else None
    }


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload

        # Basic validation for required fields (avoid 500)
        title = place_data.get('title')
        owner_id = place_data.get('owner_id')
        if not title or not isinstance(title, str) or not title.strip():
            return {'error': 'Invalid input data'}, 400
        if not owner_id or not isinstance(owner_id, str):
            return {'error': 'Invalid input data'}, 400

        try:
            new_place = facade.create_place(place_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return place_to_dict(new_place), 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        # list view can be lighter, but keep consistent
        return [{
            'id': p.id,
            'title': p.title,
            'latitude': p.latitude,
            'longitude': p.longitude,
        } for p in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place_to_dict(place), 200

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        try:
            updated = facade.update_place(place_id, place_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        if not updated:
            return {'error': 'Place not found'}, 404

        return place_to_dict(updated), 200


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        reviews = facade.get_reviews_by_place(place_id)
        return [{'id': r.id, 'text': r.text, 'rating': r.rating} for r in reviews], 200

