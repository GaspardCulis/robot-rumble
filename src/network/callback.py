from abc import ABC, abstractmethod
from asyncio import DatagramTransport

from network.connection_state import ConnectionState
from network.converter import Address


class Callback(ABC):
    @abstractmethod
    def on_connected(self, transport: DatagramTransport, state: ConnectionState, addr: Address):
        pass  # Called when a new client is connected / you are connected to the server

    @abstractmethod
    def welcome_data(self, data: bytes, state: ConnectionState, addr: Address):
        pass  # Called when you get the first data about someone

    @abstractmethod
    def on_disconnect(self, state: ConnectionState, addr: Address):
        pass  # Called when a client is disconnected / you are disconnected from the server
