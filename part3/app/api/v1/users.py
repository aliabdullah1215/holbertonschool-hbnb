from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.services.facade import HBnBFacade

facade = HBnBFacade()
api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(description='Is the user an admin', default=False)
})

update_user_model = api.model('UpdateUser', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='Password of the user')
})

@api.route('/')
class UserList(Resource):

    # --- التعديل هنا: أزلنا @jwt_required() للسماح بالتسجيل المفتوح ---
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    def post(self):
        """Create a new user (Open for registration)"""
        data = api.payload

        if facade.get_user_by_email(data['email']):
            return {'error': 'Email already registered'}, 400

        user_data = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'password': data['password'],
            'is_admin': data.get('is_admin', False) # يمكنك التحكم هنا بجعل أول مستخدم Admin
        }

        user = facade.create_user(user_data)
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'message': 'User created successfully'
        }, 201

    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """Get list of users"""
        users = facade.get_all_users()
        return [
            {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email
            }
            for u in users
        ], 200

@api.route('/<user_id>')
class UserResource(Resource):
    # ... (باقي كود UserResource يبقى كما هو دون تغيير) ...
    @api.response(200, 'User retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()
    @api.expect(update_user_model, validate=True)
    def put(self, user_id):
        # (ابقِ الكود كما هو لحماية عمليات التحديث)
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        current_user_id = get_jwt_identity()
        data = api.payload
        if not is_admin:
            if user_id != current_user_id:
                return {'error': 'Unauthorized action'}, 403
            if 'email' in data or 'password' in data:
                return {'error': 'You cannot modify email or password.'}, 400
        user = facade.update_user(user_id, data)
        if not user: return {'error': 'User not found'}, 404
        return {'id': user.id, 'message': 'User updated successfully'}, 200
