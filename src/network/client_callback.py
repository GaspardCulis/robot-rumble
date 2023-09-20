from network.callback import Callback
from network.converter import Address


class ClientCallback(Callback):
    def on_connected(self, addr: Address):
        pass

    def on_disconnect(self, addr: Address):
        pass
