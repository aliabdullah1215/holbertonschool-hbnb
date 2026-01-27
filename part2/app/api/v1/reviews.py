from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


def review_to_dict(review):
    return {
        'id': review.id,
        'text': review.text,
        'rating': review.rating,
        'user_id': review.user.id if getattr(review, 'user', None) else None,
        'place_id': review.place.id if getattr(review, 'place', None) else None,
        'created_at': review.created_at.isoformat() if hasattr(review, 'created_at') else None,
        'updated_at': review.updated_at.isoformat() if hasattr(review, 'updated_at') else None
    }


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        data = api.payload

        # prevent 500: basic required fields
        text = data.get('text')
        rating = data.get('rating')
        user_id = data.get('user_id')
        place_id = data.get('place_id')

        if not text or not isinstance(text, str) or not text.strip():
            return {'error': 'Invalid input data'}, 400
        if not isinstance(rating, int):
            return {'error': 'Invalid input data'}, 400
        if not user_id or not isinstance(user_id, str):
            return {'error': 'Invalid input data'}, 400
        if not place_id or not isinstance(place_id, str):
            return {'error': 'Invalid input data'}, 400

        try:
            review = facade.create_review({
                'text': text.strip(),
                'rating': rating,
                'user_id': user_id,
                'place_id': place_id
            })
        except ValueError as e:
            return {'error': str(e)}, 400

        return review_to_dict(review), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        # basic list per spec
        return [{'id': r.id, 'text': r.text, 'rating': r.rating} for r in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review_to_dict(review), 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        data = api.payload

        # allow partial update of text/rating (ignore user_id/place_id)
        update_data = {}
        if 'text' in data:
            if not data['text'] or not isinstance(data['text'], str) or not data['text'].strip():
                return {'error': 'Invalid input data'}, 400
            update_data['text'] = data['text'].strip()

        if 'rating' in data:
            if not isinstance(data['rating'], int):
                return {'error': 'Invalid input data'}, 400
            update_data['rating'] = data['rating']

        try:
            updated = facade.update_review(review_id, update_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        if not updated:
            return {'error': 'Review not found'}, 404

        return review_to_dict(updated), 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        deleted = facade.delete_review(review_id)
        if not deleted:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200

