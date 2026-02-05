from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# تعريف الكائنات هنا لكسر الدائرة (Circular Import)
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
