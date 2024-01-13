from instance.config import Config
from src.utils.helpers import get_url
from src.utils.responseEntity import *


class BillService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BillService, cls).__new__(cls)
        return cls._instance

    def get_bill_details(self, db, requests, provider, rates, trucks, id, t1, t2, logger=None):
        try:
            provider_data = self.get_provider_data(db, provider, id)

            if not provider_data:
                return error_response("Provider not found")

            producer_trucks_id = self.get_producer_trucks_id(trucks, provider_data)

            truck_counter, session_counter, sessions = self.get_session_counters(requests, producer_trucks_id, t1, t2)
            get_weight = self.get_weight_data(requests, t1, t2, producer_trucks_id)
            products = self.get_products(requests, db, rates, provider_data, sessions, t1, t2, get_weight)

            total = self.calculate_total(products)

            products_output = self.get_products_output(products)

            output_json = {
                "id": id,
                "name": provider_data.name,
                "from": t1,
                "to": t2,
                "truckCount": truck_counter,
                "sessionCount": session_counter,
                "products": products_output,
                "total": total
            }
            return success_response("Bill report generated successfully", output_json, logger=logger,
                                    logger_type="info")

        except Exception as e:
            return error_response(str(e), logger=logger, logger_type="error")

    def get_provider_data(self, db, provider, id):
        return db.get_or_404(provider, id)

    def get_producer_trucks_id(self, Trucks, provider_data):
        return [truck.id for truck in Trucks.query.filter_by(provider_id=provider_data.id).all()]

    def get_weight_data(self, requests, t1, t2, container):
        response = requests.get(f"{Config.weigh_url}/weight?filter=in&from={t1}&to={t2}")
        response.raise_for_status()
        filtered_data = filter(lambda x: x['truck'] in container, response.json()["data"])
        return list(filtered_data)

    def get_session_counters(self, requests, producer_trucks_id, t1, t2):
        truck_counter = 0
        session_counter = 0
        sessions = []

        for truck_id in producer_trucks_id:
            response = requests.get(get_url('item/' + str(truck_id), t1, t2))
            response.raise_for_status()
            truck_sessions = response.json()['sessions']

            if len(truck_sessions) > 0:
                truck_counter += 1
                session_counter += len(truck_sessions)

            for session in truck_sessions:
                sessions.append(session)

        return truck_counter, session_counter, sessions

    def get_products(self, requests, db, rates, provider, sessions, t1, t2, get_weight):
        products = dict()

        for session_id in sessions:
            response = requests.get(get_url(f'session/{session_id}', t1, t2))
            response.raise_for_status()
            session_data = next(
                (
                    x for x in response.json()
                    if x.get('truck') != "N/A" and x.get('truck_tara') is None
                ),
                None
            )
            weight_id = session_data['id']
            product = next((x for x in get_weight if x.get('id') == weight_id), None)
            product_id = product['produce']
            products.setdefault(product_id, [0, 0, 0, 0])
            products[product_id][0] += 1

            if product['neto'] is not None and product['neto'] > 0:
                products[product_id][1] += int(product['neto'])

        for product_name, product_data in products.items():
            price = db.session.query(rates).filter_by(product_id=product_name, scope=provider.id).first()
            if price is None:
                price = db.session.query(rates).filter_by(product_id=product_name).first()
            if price is None:
                continue
            product_data[2] = price.rate
        return products

    def calculate_total(self, products):
        total = 0
        for product_name, product_data in products.items():
            pay = product_data[1] * product_data[2]
            product_data[3] = pay
            total += pay

        return total

    def get_products_output(self, products):
        products_output = list()

        for product_name, product_data in products.items():
            products_output.append({
                "product": product_name,
                "count": product_data[0],
                "amount": product_data[1],
                "rate": product_data[2],
                "pay": product_data[3]
            })

        return products_output
