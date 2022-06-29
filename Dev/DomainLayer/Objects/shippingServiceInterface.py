#import requests


class shippingServiceInterface:

    def __init__(self, url=None):
        self.url = url
        self._demo = (url is None)
        self._demo_transaction_id_counter = 10000 - 1

    def send(self, command):
        try:
            return requests.post(self.url, command)
        except Exception:
            return "Timeout"

    def handshake(self):
        if self._demo:
            return "OK"
        else:
            command = {{"action_type": "handshake"}}
            return self.send(command)

    def supply(self, name, address, city, country, zip):
        if self._demo:
            self._demo_transaction_id_counter += 1
            return self._demo_transaction_id_counter
        else:
            command = {{"action_type": "supply"}, {"name": name}, {"address": address}, {"city": city},
                       {"country": country}, {"zip": str(zip)}}
            return self.send(command)

    def cancel_supply(self, transaction_id):
        if self._demo:
            return 1
        else:
            command = {{"action_type": "cancel_supply"}, {"transaction_id": str(transaction_id)}}
            return self.send(command)
