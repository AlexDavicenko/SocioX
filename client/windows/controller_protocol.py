
from typing import Protocol

class Controller(Protocol):
    def switch_frame(self, frame_name: str) -> None: ...