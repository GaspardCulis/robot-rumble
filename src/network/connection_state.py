import asyncio
import dataclasses
from asyncio import Task
from typing import Any


@dataclasses.dataclass(solts=True)
class ConnectionState:
    addr: tuple[str | Any, int]
    last_received_id: int = 0
    last_sent_id: int = 0
    connected: bool = False
    timeout_task: Task = None
    keepalive_task: Task = None
