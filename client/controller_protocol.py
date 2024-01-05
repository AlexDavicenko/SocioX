#This file exists to avoid cyclic imports and allow the application 
#windows to be managed by the Controller and communicate back to the Controller.
#Only functions which are called by internal objects are defined here since the
#network client interface has direct access to the Controller.
from typing import Protocol, List, Callable


import sys
sys.path.append('../')
from communication_protocol.TCPMessages import *
sys.path.append('client/')


class Controller(Protocol):
    username: str
    current_channel_id: int
    friends: List[str]

    # //// SETUP ////
    def add_binding(self, key: str, func: Callable) -> None: ...
    
    def switch_frame(self, frame_name: str) -> None: ...
    
    
    # //// Messages ////
    def add_message(self, content: str) -> None: ...


    # //// Channels ////
    def channel_create_request(self, channel_name: str): ...
    
    def add_channel(self, channel_id: int, channel_name: str): ...

    def switch_channel(self, channel_id: int): ...

    def channel_join_request(self, channel_id: int): ...

    def leave_channel(self, channel_id: int) -> None: ...
    
    # //// Friends ////
    def send_friend_request(self, username: str, firstname: str, lastname: str) -> None: ...

    def accept_friend_request(self, username: str) -> None: ...

    def reject_friend_request(self, username: str) -> None: ...

    def remove_friend(self, username: str) -> None: ...

    # //// Search ////
    def search_request(self, search: str) -> None: ...

    # //// Login ////
    def attempt_login(self, username: str, password: str) -> None: ...

    # //// Sign up ////
    def signup_request(self) -> None: ...
    
    def verify_code(self, code: str) -> None: ...

    # //// Text Suggestions ////
    def get_suggestions(self, prefix: str) -> List[str]: ...

    def on_suggestion_press(self, suggestioNo): ...


    # //// Other ////
    def close() -> None: ...
