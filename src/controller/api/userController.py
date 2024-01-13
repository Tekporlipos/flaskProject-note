from flask import request

from app import app, db
from src.models.UserModel import User
from src.services.userService import UserService
from src.utils.httpMethod import HttpMethod

providerService = UserService()


@app.route('/api/v1/register', methods=[HttpMethod.POST])
def register():
    user_data = request.json
    return providerService.create(db, User, user_data, logger=app.logger)


@app.route('/api/v1/login', methods=[HttpMethod.POST])
def login():
    user_data = request.json
    return providerService.login(User, user_data, logger=app.logger)
