from flask import request

from app import app, db
from src.models.NoteModel import Notes
from src.services.NoteService import TrunkService
from src.utils.httpMethod import HttpMethod

trunkService = TrunkService()


@app.route('/api/v1/create', methods=[HttpMethod.POST])
def create():
    return trunkService.create(db, Notes, request.json, app.logger)


@app.route('/api/v1/notes', methods=[HttpMethod.GET])
def get_notes():
    return trunkService.get_notes(db, Notes, app.logger)

@app.route('/api/v1/notes/<note_id>', methods=[HttpMethod.GET])
def get_notes_by_id(note_id):
    return trunkService.get_notes(db, Notes,note_id, app.logger)

@app.route('/api/v1/notes/<note_id>', methods=[HttpMethod.PATCH])
def update_notes_by_id(note_id):
    return trunkService.update_notes_by_id(db, Notes, note_id, request.json, app.logger)


@app.route('/api/v1/notes/<note_id>', methods=[HttpMethod.DELETE])
def delete_notes_by_id(note_id):
    return trunkService.delete_notes_by_id(db, Notes, note_id, app.logger)
