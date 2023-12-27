from typing import Dict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TCPMessage:
    pass
 
#Connection Messages:

@dataclass
class ConnectionMessage(TCPMessage):
    status: bool

@dataclass
class ConnectionEstablished(ConnectionMessage):
    pass

@dataclass
class ConnectionClosed(ConnectionMessage):
    pass

#Client Messages:

@dataclass
class ClientMessage(TCPMessage):
    pass

@dataclass
class TextMessage(ClientMessage):
    channel_id: int
    content: str

@dataclass
class NewMessageNotif(ClientMessage):
    time_sent: datetime
    channel_id: int
    content: str
    sender_name: str

@dataclass
class FriendRequest(ClientMessage):
    username: str
        
@dataclass
class FriendRequestNotif(ClientMessage):
    username: str
    firstname: str
    lastname: str

@dataclass
class FriendRequestDecision(ClientMessage):
    success: bool
    username: str

@dataclass
class FriendRemoval(ClientMessage):
    username: str

@dataclass
class FriendRemovedNotif(ClientMessage):
    username: str

@dataclass 
class FriendStatusNotif(ClientMessage):
    username: str
    firstname: str
    lastname: str
    decision: str

@dataclass
class ChannelJoinRequest(ClientMessage):
    channel_id: int

@dataclass
class ChannelCreateRequest(ClientMessage):
    channel_name: str

@dataclass
class ChannelCreateResponse(ClientMessage):
    success: bool
    channel_id: int
    channel_name: str

@dataclass
class ChannelJoinResponse(ClientMessage):
    success: bool
    channel_id: int
    channel_name: str

@dataclass
class ChannelLeave(ClientMessage):
    channel_id: int

@dataclass
class ChannelLeaveNotif(ClientMessage):
    channel_id: int
    username: str

@dataclass
class UserJoinNotif(ClientMessage):
    channel_id: int
    username: str
    firstname: str
    lastname: str

@dataclass
class SearchRequest(ClientMessage):
    content: str

@dataclass
class SearchReponse(ClientMessage):
    response_data: list

#Auth Messages:
@dataclass
class AuthMessage(TCPMessage):
    pass

@dataclass
class LoginAttempt(AuthMessage):
    username: str

@dataclass
class LoginResponse(AuthMessage):
    success: bool
    user_id: int
    username: str
    firstname: str
    lastname: str
    email: str
    dob: datetime
    account_created: datetime

@dataclass
class SignUpAttempt(AuthMessage):
    username: str
    firstname: str
    lastname: str
    email: str
    password: str
    dob: datetime


class CodeLookUp:
    MessageCodeToTCPMessageClass: Dict[int, TCPMessage] = {
    0: TCPMessage,
    101: ConnectionMessage,
    102: ConnectionEstablished,
    103: ConnectionClosed,
    200: ClientMessage,
    201: TextMessage,
    202: NewMessageNotif,
    203: FriendRequest,
    204: FriendRequestDecision,
    205: ChannelJoinRequest,
    206: ChannelCreateRequest,
    207: ChannelCreateResponse,
    208: ChannelJoinResponse,
    209: UserJoinNotif,
    300: AuthMessage,
    301: LoginAttempt,
    302: LoginResponse,
    303: SignUpAttempt

    }

    TCPMessageClassToMessageCode: Dict[TCPMessage, int] = {
    TCPMessage: 0,
    ConnectionMessage: 101,
    ConnectionEstablished: 102,
    ConnectionClosed: 103,
    ClientMessage: 200,
    TextMessage: 201,
    NewMessageNotif: 202,
    FriendRequest: 203,
    FriendRequestDecision: 204,
    ChannelJoinRequest: 205,
    ChannelCreateRequest: 206,
    ChannelCreateResponse: 207,
    ChannelJoinResponse: 208,
    UserJoinNotif: 209,
    AuthMessage: 300,
    LoginAttempt: 301,
    LoginResponse: 302,
    SignUpAttempt: 303

    }


