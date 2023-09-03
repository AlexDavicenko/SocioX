import copy
import logging
import datetime

from typing import List, Dict, Any
from dataAccessLayer import DataAccessLayer

import sys; sys.path.append('../')
from communication_protocol.TCPMessages import *



class Controller:
    def __init__(self) -> None:

        self.client_ids: List[int] = []
        self.client_id_user_id_map: Dict[int, int] = {}
        self.user_id_client_id_map: Dict[int, int] = {}

        self.dal = DataAccessLayer('chatapp')

        #Client ID: List[Message Object]
        self.messages: Dict[int, List[TCPMessage]]= {}
        

    def get_new_messages(self, client_id: int) -> List[TCPMessage]:
        #Get all the messages for the specific client ID
        new_msgs: List[TCPMessage] = self.messages.get(client_id, [])
        
        
        if new_msgs:    
            #Clear all the messages that are about to be sent out
            self.messages[client_id] = []
        
        return new_msgs

    def handle_message(self, msg: TCPMessage, client_id):
        
        

        if isinstance(msg, TextMessage):
            user_id = self.client_id_user_id_map[client_id]
            self.dal.add_message(msg.channel_id, msg.content, user_id)
            sender_data = self.dal.get_user_data(user_id)[0]

            users = self.dal.get_channel_users(msg.channel_id)
            for user in users:
                #Determine who needs to be notified about the message
                print(f"notif added: {user['Username']}")
                self.add_message_by_id(self.user_id_client_id_map[user['UserID']], NewMessageNotif(
                    time_sent=datetime.now(),
                    channel_id=msg.channel_id,
                    content=msg.content,
                    sender_name=sender_data['Username']
                ))

        elif isinstance(msg, ConnectionClosed):
            pass


        elif isinstance(msg, LoginAttempt):
            user_id = self.dal.get_user_id(msg.username)            
            if user_id == None:
                self.add_message_by_id(client_id, LoginResponse(
                    ip=0,
                    success=False
                ))
            else:
                #save the client_id -> user_id mapping
                self.client_id_user_id_map[client_id] = user_id
                self.user_id_client_id_map[user_id] = client_id

                self.add_message_by_id(client_id, LoginResponse(
                    ip=0,
                    success=True
                ))

        elif isinstance(msg, ChannelJoinRequest):
            user_id = self.client_id_user_id_map[client_id]
            self.dal.add_user_channel_connection(msg.channel_id, user_id)
            channel_data = self.dal.get_channel_data(msg.channel_id)[0]

            self.add_message_by_id(client_id, ChannelAddResponse(
                success = True,
                channel_id = msg.channel_id,
                channel_name= channel_data['ChannelName']
            ))

        elif isinstance(msg, ChannelCreateRequest):
            
            user_id = self.client_id_user_id_map[client_id]

            channel_id = self.dal.add_channel(msg.channel_name, user_id)
            channel_data = self.dal.get_channel_data(channel_id)[0]

            self.add_message_by_id(client_id, ChannelAddResponse(
                success=True,
                channel_id=channel_id,
                channel_name= channel_data['ChannelName']
            ))


    
    def add_message_by_id(self, client_id: int, msg: TCPMessage):
        new_msgs = self.messages.get(client_id, []) + [msg] 
        self.messages[client_id] = new_msgs

        