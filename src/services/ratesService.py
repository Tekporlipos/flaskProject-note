from src.utils.responseEntity import *


class RatesService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RatesService, cls).__new__(cls)
        return cls._instance

    def read_excel_file(self, os, pd, file_path):
        if not os.path.exists(file_path):
            return None, "File not found on the server"
        rates_df = pd.read_excel(file_path)
        return rates_df, None

    def process_and_update_rates(self, integrityError, db, rates, rates_df):
        last_record_id = db.session.query(rates.id).order_by(rates.id.desc()).first()
        last_record_id = last_record_id[0] if last_record_id else 0
        for _, row in rates_df.iterrows():
            product_id = row['Product']
            rate = row['Rate']
            scope = row['Scope']
            try:
                new_rate = rates(product_id=product_id, rate=rate, scope=scope)
                db.session.add(new_rate)
                db.session.commit()
            except integrityError:
                db.session.rollback()
        db.session.query(rates).filter(rates.id <= last_record_id).delete()
        db.session.commit()
        return last_record_id

    def upload_rates(self, integrity_error, db, rates, os, pd, request, logger=None):
        try:
            if 'file' not in request:
                return error_response("No file name provided in the request body", logger=logger, logger_type="warning")
            file_name = request.get('file')
            file_path = os.path.join('in/', file_name)
            rates_df, file_error = self.read_excel_file(os, pd, file_path)
            if file_error:
                return error_response(file_error)
            self.process_and_update_rates(integrity_error, db, rates, rates_df)
            return success_response("Rates uploaded successfully", logger=logger, logger_type="info")
        except Exception as e:
            return error_response(str(e), status_code=500, logger=logger, logger_type="error")

    def download_rates(self, pd, rates, send_file, logger=None):
        try:
            rates_data = rates.query.all()
            serialized_data = {
                "Product": [rate.product_id for rate in rates_data],
                "Rate": [rate.rate for rate in rates_data],
                "Scope": [int(rate.scope) if rate.scope.isdigit() else rate.scope for rate in rates_data]
            }
            rates_df = pd.DataFrame(serialized_data, columns=['Product', 'Rate', 'Scope'])
            excel_file_path = '/tmp/rates_export.xlsx'
            rates_df.to_excel(excel_file_path, index=False)
            if logger is not None:
                logger.info('rates_export.xlsx exported')
            return send_file(excel_file_path, as_attachment=True, download_name='rates_export.xlsx')
        except Exception as e:
            return error_response(str(e), status_code=500, logger=logger, logger_type="error")
