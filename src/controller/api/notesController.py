from flask import request

from app import app, db
from src.models.NoteModel import Notes
from src.services.NoteService import NoteService
from src.utils.httpMethod import HttpMethod

noteService = NoteService()


@app.route('/api/v1/note', methods=[HttpMethod.POST])
def create():
    return noteService.create(db, Notes, request.json, app.logger)


@app.route('/api/v1/note', methods=[HttpMethod.GET])
def get_notes():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    return noteService.get_notes(db, Notes, page=page, page_size=page_size, logger=app.logger)


@app.route('/api/v1/note/<note_id>', methods=[HttpMethod.GET])
def get_notes_by_id(note_id):
    return noteService.get_notes_by_id(db, Notes, note_id, app.logger)


@app.route('/api/v1/note/<note_id>', methods=[HttpMethod.PATCH])
def update_notes_by_id(note_id):
    return noteService.update_notes_by_id(db, Notes, note_id, request.json, app.logger)


@app.route('/api/v1/note/<note_id>', methods=[HttpMethod.DELETE])
def delete_notes_by_id(note_id):
    return noteService.delete_notes_by_id(db, Notes, note_id, app.logger)
