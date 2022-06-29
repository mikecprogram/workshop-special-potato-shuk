class shippingServiceInterface:

    def __init__(self, url=None):
        self._demo = (url is None)
        self._demo_transaction_id_counter = 10000 - 1

    def handshake(self):
        if self._demo:
            return "OK"
        else:
            pass

    def supply(self, name, address, city, country, zip):
        if self._demo:
            self._demo_transaction_id_counter += 1
            return self._demo_transaction_id_counter
        else:
            pass


    def cancel_supply(self, transaction_id):
        if self._demo:
            return 1
        else:
            pass
