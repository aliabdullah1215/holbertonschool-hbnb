from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

review_model = api.model('Review', {
    'place_id': fields.String(required=True, description='ID of the place'),
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)', min=1, max=5)
})

@api.route('/')
class ReviewList(Resource):

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return [
            {
                'id': r.id,
                'text': r.text,
                'rating': r.rating,
                'place_id': r.place_id,
                'user_id': r.user_id,
                'user_name': f"{r.user.first_name} {r.user.last_name}" if hasattr(r, 'user') and r.user else "Anonymous User"
            } for r in reviews
        ], 200

    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review created successfully')
    @api.response(400, 'Invalid input or business logic error')
    @api.response(404, 'Place not found')
    def post(self):
        """Create a review (authenticated users only)"""
        current_user_id = get_jwt_identity()
        data = api.payload

        # 1. التأكد من وجود المكان
        place = facade.get_place(data['place_id'])
        if not place:
            print(f"DEBUG: Place {data['place_id']} not found.")
            return {'error': 'Place not found'}, 404

        # 2. منع المالك من تقييم مكانه الخاص
        # قمنا بإضافة طباعة للتيرمينال للتأكد إذا كان هذا هو سبب الـ 400
        if str(place.owner_id) == str(current_user_id):
            print(f"REJECTED: User {current_user_id} is the owner of place {place.id}")
            return {'error': 'You cannot review your own place.'}, 400

        # 3. منع التكرار (مراجعة واحدة لكل مستخدم لكل مكان)
        all_reviews = facade.get_all_reviews()
        if any(str(r.place_id) == str(data['place_id']) and str(r.user_id) == str(current_user_id) for r in all_reviews):
            print(f"REJECTED: User {current_user_id} already reviewed place {data['place_id']}")
            return {'error': 'You have already reviewed this place.'}, 400

        # 4. ربط التقييم بالمستخدم صاحب التوكن آلياً
        data['user_id'] = current_user_id
        
        try:
            new_review = facade.create_review(data)
            return {
                'id': new_review.id,
                'message': 'Review created successfully'
            }, 201
        except Exception as e:
            print(f"DEBUG: Error in facade.create_review: {str(e)}")
            return {'error': str(e)}, 400

@api.route('/<review_id>')
class ReviewResource(Resource):

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'place_id': review.place_id,
            'user_id': review.user_id,
            'user_name': f"{review.user.first_name} {review.user.last_name}" if hasattr(review, 'user') and review.user else "Anonymous User"
        }, 200

    @jwt_required()
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review (owner or admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin and str(review.user_id) != str(current_user_id):
            return {'error': 'Unauthorized action'}, 403

        facade.update_review(review_id, api.payload)
        return {'message': 'Review updated successfully'}, 200

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review (owner or admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin and str(review.user_id) != str(current_user_id):
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200
    