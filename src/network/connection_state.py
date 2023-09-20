import dataclasses
from typing import Any


@dataclasses.dataclass
class ConnectionState:
    addr: tuple[str | Any, int]
    last_recieved_id: int = 0
    last_sent_id: int = 0
    connected: bool = False