from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services.facade import HBnBFacade

api = Namespace('auth', description='Authentication operations')
facade = HBnBFacade()

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class LoginResource(Resource):
    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful, token returned')
    @api.response(401, 'Invalid email or password')
    def post(self):
        """Login and receive a JWT token"""
        data = api.payload
        
        # استرجاع المستخدم عبر البريد الإلكتروني
        user = facade.get_user_by_email(data['email'])

        # التحقق من وجود المستخدم ومطابقة كلمة المرور
        if user and user.verify_password(data['password']):
            # ملاحظة: في النسخ الحديثة من Flask-JWT-Extended، يفضل أن تكون الهوية string
            access_token = create_access_token(
                identity=str(user.id), 
                additional_claims={'is_admin': user.is_admin}
            )
            return {'access_token': access_token}, 200
        
        return {'error': 'Invalid email or password'}, 401
