from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

# Request model
review_model = api.model('Review', {
    'place_id': fields.String(required=True, description='ID of the place'),
    'text': fields.String(required=True, description='Review text')
})


@api.route('/')
class ReviewList(Resource):

    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review created successfully')
    @api.response(400, 'Invalid review')
    @api.response(404, 'Place not found')
    def post(self):
        """Create a review (authenticated users only)"""
        current_user_id = get_jwt_identity()
        data = api.payload

        # Get place
        place = facade.get_place(data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404

        # ❌ User cannot review own place
        if place.owner_id == current_user_id:
            return {'error': 'You cannot review your own place.'}, 400

        # ❌ User cannot review same place twice
        for review in facade.get_all_reviews():
            if review.place_id == data['place_id'] and review.user_id == current_user_id:
                return {'error': 'You have already reviewed this place.'}, 400

        review = facade.create_review({
            'text': data['text'],
            'place_id': data['place_id'],
            'user_id': current_user_id
        })

        return {
            'id': review.id,
            'message': 'Review created successfully'
        }, 201


@api.route('/<review_id>')
class ReviewResource(Resource):

    @jwt_required()
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review (owner only)"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        if review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        updated_review = facade.update_review(review_id, api.payload)

        return {
            'id': updated_review.id,
            'text': updated_review.text
        }, 200

    @jwt_required()
    @api.response(204, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review (owner only)"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        if review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return {}, 204
