from datetime import datetime

import requests as fetch
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import app, db
from src.models.UserModel import User
from src.models.NoteModel import Notes
from src.services.trunkService import TrunkService
from src.utils.httpMethod import HttpMethod

trunkService = TrunkService()


@app.route('/api/v1/create', methods=[HttpMethod.POST])
@jwt_required()
def create():
    current_user = get_jwt_identity()
    return trunkService.register_truck(db, User, Notes, request.json, app.logger)


@app.route('/api/v1/notes', methods=[HttpMethod.GET])
@jwt_required()
def get_notes_by_id(user_id):
    current_user = get_jwt_identity()
    return trunkService.register_truck(db, User, Notes, request.json, app.logger)


@app.route('/api/v1/notes/<note_id>', methods=[HttpMethod.PATCH])
@jwt_required()
def update_notes_by_id(note_id):
    current_user = get_jwt_identity()
    return trunkService.register_truck(db, User, Notes, request.json, app.logger)


@app.route('/api/v1/notes/<note_id>', methods=[HttpMethod.DELETE])
@jwt_required()
def delete_notes_by_id(note_id):
    current_user = get_jwt_identity()
    return trunkService.register_truck(db, User, Notes, request.json, app.logger)

