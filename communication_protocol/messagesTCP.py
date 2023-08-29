from datetime import datetime
from enum import Enum
import pickle
from typing import Dict


class TCPMessage:
        
    def __init__(self) -> None:
        pass

    @classmethod
    def reconstruct(cls, **kwargs):
        cls.__dict__.update(kwargs)
    
    

class AuthMessage(TCPMessage):
    def __init__(self) -> None:
        super().__init__()

        
class ConnectionMessage(TCPMessage):
    def __init__(self) -> None:
        super().__init__()

class ClientMessage(TCPMessage):
    def __init__(self, client_id: int) -> None:
        super().__init__()
        self.client_id = client_id
        
class TextMessage(ClientMessage):
    def __init__(self, client_id: int, channel_id: int, text) -> None:
        super().__init__(client_id)
        self.channel_id = channel_id
        self.text = text


class NewMessageNotif(ClientMessage):
    def __init__(self, client_id: int, channel_id: int, text) -> None:
        super().__init__(client_id)
        self.channel_id = channel_id
        self.text = text

        


class FriendRequest(ClientMessage):
    def __init__(self) -> None:
        super().__init__()


class AcceptedFriendRequest(ClientMessage):
    def __init__(self) -> None:
        super().__init__()


class ConnectionEstablished(ConnectionMessage):
    def __init__(self) -> None:
        super().__init__()

class ConnectionClosed(ConnectionMessage):
    def __init__(self) -> None:
        super().__init__()

class CodeLookUp:
    MessageCodeToTCPMessageClass: Dict[int, TCPMessage] = {
    0: TCPMessage,
    1: ClientMessage,
    2: TextMessage,
    3: NewMessageNotif
    }

    TCPMessageClassToMessageCode: Dict[TCPMessage, int] = {
        TCPMessage: 0,
        ClientMessage: 1,
        TextMessage: 2,
        NewMessageNotif: 3
    }
    
"""
c, t =  CodeLookUp.TCPMessageClassToMessageCode[TCPMessage], TextMessage(10,32)


pickled = pickle.dumps((c, t))
print(pickled)

# pickled is now a bytes object that contains the pickled representation of data
print(pickled.__sizeof__())
print(type(pickled))



restored = pickle.loads(pickled)
print(restored)
"""



