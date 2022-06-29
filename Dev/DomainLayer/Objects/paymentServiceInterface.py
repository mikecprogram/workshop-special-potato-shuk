#import requests


class paymentServiceInterface:
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

    def pay(self, card_number, month, year, holder, ccv, id):
        if self._demo:
            self._demo_transaction_id_counter += 1
            return self._demo_transaction_id_counter
        else:
            command = {{"action_type": "pay"}, {"card_number": str(card_number)}, {"month": str(month)},
                       {"year": str(year)}, {"holder": holder}, {"ccv": str(ccv)}, {"id": str(id)}}
            return self.send(command)

    def cancel_pay(self, transaction_id):
        if self._demo:
            return 1
        else:
            command = {{"action_type": "cancel_pay"}, {"transaction_id": str(transaction_id)}}
            return self.send(command)
