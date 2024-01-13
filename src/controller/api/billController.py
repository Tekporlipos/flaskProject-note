from datetime import datetime

import requests as fetch
from flask import request

from app import app, db
from src.models.UserModel import User
from src.models.RatesModel import Rates
from src.models.NoteModel import Notes
from src.services.billService import BillService
from src.utils.httpMethod import HttpMethod

billService = BillService()


@app.route('/api/v1/bill/<id>', methods=[HttpMethod.GET])
def get_bill(id):
    t1 = request.args.get('from', default=datetime.now()
                          .replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                          .strftime('%Y%m%d%H%M%S'))
    t2 = request.args.get('to', default=datetime.now().strftime('%Y%m%d%H%M%S'))
    return billService.get_bill_details(db, fetch, User, Rates, Notes, id, t1, t2, logger=app.logger)
