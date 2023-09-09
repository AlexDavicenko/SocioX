import copy
import logging
from datetime import datetime

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
                if user['UserID'] != user_id:
                    #Checking if the user is currently still connected
                    if user['UserID'] in self.user_id_client_id_map: 
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
                self.update_client(client_id)


        elif isinstance(msg, ChannelJoinRequest):
            user_id = self.client_id_user_id_map[client_id]
            #TODO: check if channel exists
            self.dal.add_user_channel_connection(msg.channel_id, user_id)
            channel_data = self.dal.get_channel_data(msg.channel_id)[0]
            self.add_message_by_id(client_id, ChannelAddResponse(
                success = True,
                channel_id = msg.channel_id,
                channel_name= channel_data['ChannelName']
            ))
            self.update_user_on_channel_messages(client_id, msg.channel_id)
            self.update_user_on_channel_members(client_id, msg.channel_id)
            self.update_users_on_user_join(client_id, msg.channel_id)

        elif isinstance(msg, ChannelCreateRequest):
            
            user_id = self.client_id_user_id_map[client_id]

            channel_id = self.dal.add_channel(msg.channel_name, user_id)
            self.dal.add_user_channel_connection(channel_id, user_id)
            channel_data = self.dal.get_channel_data(channel_id)[0]

            self.add_message_by_id(client_id, ChannelAddResponse(
                success=True,
                channel_id=channel_id,
                channel_name= channel_data['ChannelName']
            ))


    
    def add_message_by_id(self, client_id: int, msg: TCPMessage):
        new_msgs = self.messages.get(client_id, []) + [msg] 
        self.messages[client_id] = new_msgs

    
    def update_user_on_channel_messages(self, client_id: int, channel_id: int):
        for message in self.dal.get_channels_messages(channel_id):
            self.add_message_by_id(client_id, NewMessageNotif(
                time_sent=message['DateSent'],
                channel_id=channel_id,
                content=message['Content'],
                sender_name=message['Username']
            ))

    def update_user_on_channel_members(self, client_id: int, channel_id: int):
        user_id = self.client_id_user_id_map[client_id]
        
        for user in self.dal.get_channel_users(channel_id):
            #Does not notify the same user
            if user_id != user['UserID']:
                self.add_message_by_id(client_id, ChannelUserJoinNotif(channel_id, user['Username']))

    def update_users_on_user_join(self, client_id: int, channel_id: int):

        user_id = self.client_id_user_id_map[client_id]
        username = self.dal.get_user_data(user_id)['Username']

        for user in self.dal.get_channel_users(channel_id):
            #Does not notify the same user
            if user_id != user['UserID']:
                #if currently online
                if user_id in self.user_id_client_id_map:
                    self.add_message_by_id(self.user_id_client_id_map[user_id], ChannelUserJoinNotif(channel_id, username))


    def update_client(self, client_id: int):

        user_id = self.client_id_user_id_map[client_id]
        for channel in self.dal.get_user_channels(user_id):
            channel_id = channel['ChannelID']
            self.add_message_by_id(client_id, ChannelAddResponse(
                success = True,
                channel_id = channel_id,
                channel_name = channel['ChannelName']
            ))

            #TODO: 
            self.update_user_on_channel_messages(client_id, channel_id)
            self.update_user_on_channel_members(client_id, channel_id)