from src.utils.responseEntity import *
from werkzeug.security import generate_password_hash

class ProviderService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProviderService, cls).__new__(cls)
        return cls._instance

    def register(self, db, user, data, logger=None):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if not username or not email or not password:
            return error_response('Username, email, and password are required',
                                  status_code=400, logger=logger, logger_type="error")
        try:
            hashed_password = generate_password_hash(password, method='sha256')
            new_user = user(username=username, email=email, password_hash=hashed_password)
            db.session.add(new_user)
            return success_response('Provider created successfully', {"id": provider_id}, status_code=201,
                                    logger=logger, logger_type="info")
        except Exception as e:
            db.session.rollback()
            return error_response(str(e), status_code=400, logger=logger, logger_type="error")

    def update(self, db, provider, id, data, logger=None):
        try:
            name = data.get('name')
            if len(name.strip()) < 3:
                return error_response('Invalid name provided', status_code=400, logger=logger, logger_type="warning")
            provider_data = provider.query.get(id)
            if not provider_data:
                return error_response('Provider not found')
            provider_data.name = data.get('name', provider_data.name)
            db.session.commit()
            return success_response('Provider updated successfully', {"id": provider_data.id}, status_code=200,
                                    logger=logger, logger_type="info")
        except Exception as e:
            db.session.rollback()
            return error_response(str(e), status_code=500, logger=logger, logger_type="error")
