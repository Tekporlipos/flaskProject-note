from src.utils.helpers import get_url
from src.utils.responseEntity import error_response, success_response


class TrunkService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TrunkService, cls).__new__(cls)
        return cls._instance

    def register_truck(self, db, provider, trucks, data, logger=None):
        try:
            provider = db.get_or_404(provider, data.get("provider"))
            if not provider:
                return error_response('Provider not found', logger=logger, logger_type="warning")
            truck = trucks(id=data.get("id"), provider_id=provider.id)
            db.session.add(truck)
            truck_data = db.session.commit()
            return success_response("Truck registered successfully", truck_data,
                                    status_code=201, logger=logger, logger_type="info")
        except Exception as e:
            db.session.rollback()
            return error_response(str(e), logger=logger, logger_type="error")

    def update_truck(self, db, trucks, provider, truck_id, data, logger=None):
        try:
            truck_data = db.get_or_404(trucks, truck_id)
            if not truck_data:
                return error_response('Truck not found', logger=logger, logger_type="warning")
            provider = db.get_or_404(provider, data.get('provider'))
            if not provider:
                return error_response('Provider not found', logger=logger, logger_type="warning")
            truck_data.provider_id = provider.id
            db.session.commit()
            return success_response('Truck updated successfully', logger=logger, logger_type="info")
        except Exception as e:
            db.session.rollback()
            return error_response(str(e), logger=logger, logger_type="error")

    def get_truck_details(self, requests, db, trucks, truck_id, t1_str, t2_str, logger=None):
        try:
            truck = db.get_or_404(trucks, truck_id)
            if not truck:
                return error_response("Truck not found", logger=logger, logger_type="warning")
            response = requests.get(get_url('item/' + str(truck_id), t1_str, t2_str))
            return success_response("Trucks data", response.json(), logger=logger, logger_type="info")
        except Exception as e:
            return error_response(str(e), logger=logger, logger_type="error")
