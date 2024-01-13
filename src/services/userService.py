from flask_jwt_extended import create_access_token

from src.utils.responseEntity import *
from werkzeug.security import generate_password_hash, check_password_hash


class UserService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserService, cls).__new__(cls)
        return cls._instance

    def register(self, db, user, data, logger=None):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if not username or not email or not password:
            return error_response('Username, email, and password are required',
                                  status_code=400, logger=logger, logger_type="error")
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = user(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        try:
            db.session.commit()
            return error_response('User registered successfully',
                                  status_code=201, logger=logger, logger_type="error", data=new_user)
        except Exception as e:
            db.session.rollback()
            return error_response('Error registering user',
                                  status_code=201, logger=logger, logger_type="error", data=str(e))

    def login(self, user, data, logger=None):
        username = data.get('username')
        password = data.get('password')

        user_data = user.query.filter_by(username=username).first()
        if not user_data or not check_password_hash(user.password_hash, password):
            return error_response('Invalid username or password',
                                  status_code=401, logger=logger, logger_type="error")
        access_token = create_access_token(identity=user.id)
        return error_response('Error registering user',
                              status_code=200, logger=logger, logger_type="error", data=access_token)