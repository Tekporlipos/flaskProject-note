from src.utils.responseEntity import error_response, success_response


class NoteService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NoteService, cls).__new__(cls)
        return cls._instance

    def create(self, db, notes, data, logger=None):
        title = data.get('title')
        body = data.get('body')
        note = db.session.query(notes).filter_by(title=title).first()
        if note:
            return error_response('Note with title ' + title + ' found. You are not allowed to create duplicate notes.',
                                  logger=logger, logger_type="warning")

        new_note = notes(body=body, title=title)
        db.session.add(new_note)
        try:
            db.session.commit()
            serialized_note = {
                'id': str(new_note.id),
                'title': new_note.title,
                'body': new_note.body,
                'created_at': new_note.created_at.isoformat(),
                'updated_at': new_note.updated_at.isoformat()
            }
            return success_response("Note created successfully", serialized_note,
                                    status_code=201, logger=logger, logger_type="info")
        except Exception as e:
            db.session.rollback()
            return error_response(str(e), logger=logger, logger_type="error")

    def get_notes(self, db, notes_model, logger=None):
        try:

            notes_data = db.session.query(notes_model).all()

            serialized_notes = [
                {
                    'id': str(note.id),
                    'title': note.title,
                    'body': note.body,
                    'created_at': note.created_at.isoformat(),
                    'updated_at': note.updated_at.isoformat()
                }
                for note in notes_data
            ]

            return success_response('Notes retrieved successfully', logger=logger, logger_type="info",
                                    data={'notes': serialized_notes})
        except Exception as e:
            return error_response(str(e), logger=logger, logger_type="error")

    def get_notes_by_id(self, db, notes_model, note_id, logger=None):
        try:
            note = db.session.query(notes_model).get_or_404(note_id)
            if not note:
                return error_response("Note not found", logger=logger, logger_type="warning")
            serialized_note = {
                'id': str(note.id),
                'title': note.title,
                'body': note.body,
                'created_at': note.created_at.isoformat(),
                'updated_at': note.updated_at.isoformat()
            }
            return success_response("Note retrieved successfully", serialized_note, logger=logger, logger_type="info")
        except Exception as e:
            return error_response(str(e), logger=logger, logger_type="error")

    def update_notes_by_id(self, db, notes_model, note_id, data, logger=None):
        body = data.get('body')

        try:
            note = db.session.query(notes_model).get_or_404(note_id)
        except Exception as e:
            return error_response(str(e), logger=logger, logger_type="error")

        if not note:
            return error_response("Note not found", logger=logger, logger_type="warning")
        note.body = body
        try:
            db.session.commit()
            serialized_note = {
                'id': str(note.id),
                'title': note.title,
                'body': note.body,
                'created_at': note.created_at.isoformat(),
                'updated_at': note.updated_at.isoformat()
            }
            return success_response("Note updated successfully", serialized_note,
                                    status_code=200, logger=logger, logger_type="info")
        except Exception as e:
            db.session.rollback()
            return error_response(str(e), logger=logger, logger_type="error")

    def delete_notes_by_id(self, db, notes_model, note_id, logger=None):
        try:
            note = db.session.query(notes_model).get_or_404(note_id)
            if not note:
                return error_response("Note not found", logger=logger, logger_type="warning")

            db.session.delete(note)
            db.session.commit()

            return success_response("Note deleted successfully", logger=logger, logger_type="info")
        except Exception as e:
            db.session.rollback()
            return error_response(str(e), logger=logger, logger_type="error")
