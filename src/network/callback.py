from abc import ABC, abstractmethod

from network.converter import Address


class Callback(ABC):
    @abstractmethod
    def on_connected(self, addr: Address):
        pass  # Called when a new client is connected / you are connected to the server

    @abstractmethod
    def on_disconnect(self, addr: Address):
        pass  # Called when a client is disconnected / you are disconnected from the server

