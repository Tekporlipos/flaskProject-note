# import os
#
# from flask import request
# from flask import send_file
# from mysql.connector import IntegrityError
#
# from app import app, db
# from src.models.RatesModel import Rates
# from src.services.ratesService import RatesService
# from src.utils.httpMethod import HttpMethod
#
# ratesService = RatesService()
#
#
# @app.route('/api/v1/rates', methods=[HttpMethod.POST])
# def rate():
#     return ratesService.upload_rates(IntegrityError, db, Rates, os, pd, request=request.json, logger=app.logger)
#
#
# @app.route('/api/v1/rates', methods=[HttpMethod.GET])
# def get_rate():
#     return ratesService.download_rates(pd, Rates, send_file, logger=app.logger)
