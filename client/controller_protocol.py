#<This file exists to avoid cyclic imports and allow the application windows be managed by the Controller and communicate back to the controller>

from typing import Protocol, List


import sys
sys.path.append('../')
from communication_protocol.TCPMessages import *
sys.path.append('client/')


class Controller(Protocol):
    client_id: int
    client_username: str
    
    def switch_frame(self, frame_name: str) -> None: ...

    def recieve_incoming_msg(msg: NewMessageNotif) -> None: ...

    def get_outgoing_msgs() -> List[TCPMessage]: ...

    def add_outgoing_text_msg(msgs: str) -> None: ...
    
    def close() -> None: ...

    def channel_create_request(self, channel_name: str): ...
    
    def add_channel(self, channel_id: int, channel_name: str): ...

    def switch_channel(self, channel_id: int): ...

    def channel_join_request(self, channel_id: int): ...

    def attempt_login(self, name: str) -> None: ...

    def login_approved(self, client_id: int, client_username: str) -> None: ...

