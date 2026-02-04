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

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    def post(self):
        """Create a new user (Open for registration)"""
        data = api.payload

        if facade.get_user_by_email(data['email']):
            return {'error': 'Email already registered'}, 400

        user = facade.create_user(data)
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'message': 'User created successfully'
        }, 201

    @jwt_required()
    @api.response(200, 'Users retrieved successfully')
    @api.response(403, 'Admin privileges required')
    def get(self):
        """Get list of users (Admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        users = facade.get_all_users()
        return [
            {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email
            } for u in users
        ], 200

@api.route('/<user_id>')
class UserResource(Resource):

    @jwt_required()
    @api.response(200, 'User retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user by ID (Authenticated users only)"""
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
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input or restricted fields')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user details (Owner or Admin)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        data = api.payload

        # 1. منع المستخدم من تعديل بيانات غيره إلا إذا كان أدمن
        if not is_admin and user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        # 2. قيود المستخدم العادي: لا يمكنه تغيير الإيميل أو كلمة المرور في هذا المسار
        if not is_admin:
            if 'email' in data or 'password' in data:
                return {'error': 'You cannot modify email or password.'}, 400

        # 3. في حالة الأدمن يحاول تغيير الإيميل لمستخدم آخر، يجب التأكد من عدم التكرار
        if is_admin and 'email' in data:
            existing_user = facade.get_user_by_email(data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        user = facade.update_user(user_id, data)
        if not user:
            return {'error': 'User not found'}, 404
            
        return {'id': user.id, 'message': 'User updated successfully'}, 200
