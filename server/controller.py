import copy
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from typing import List, Dict, Any
from dataAccessLayer import DataAccessLayer

import sys; sys.path.append('../')
from communication_protocol.TCPMessages import *


#Client IDs are assigned on user connect whereas User IDs are assigned on login
#Therefore there exists a bijection between Client Ids and UserIDs
class Controller:
    def __init__(self) -> None:

        self.client_ids: List[int] = []
        self.client_id_user_id_map: Dict[int, int] = {}
        self.user_id_client_id_map: Dict[int, int] = {}
        self.dal = DataAccessLayer('chatapp', 'chatapp.csv')
        

        #Client ID: List[Message Object]
        self.messages: Dict[int, List[TCPMessage]]= {}


    # //// Helper ////

    def add_message_by_id(self, client_id: int, msg: TCPMessage):
        new_msgs = self.messages.get(client_id, []) + [msg] 
        self.messages[client_id] = new_msgs


    # //// Text messages ////

    def get_new_messages(self, client_id: int) -> List[TCPMessage]:
        #Get all the messages for the specific client ID
        new_msgs: List[TCPMessage] = self.messages.get(client_id, [])
        
        
        if new_msgs:    
            #Clear all the messages that are about to be sent out
            self.messages[client_id] = []
        
        return new_msgs
    
    

    #//// Channels ////
    
    #Runs on a channel join or user login
    def update_user_on_channel_messages(self, client_id: int, channel_id: int):
        for message in self.dal.get_channels_messages(channel_id):
            self.add_message_by_id(client_id, NewMessageNotif(
                time_sent=message['DateSent'],
                channel_id=channel_id,
                content=message['Content'],
                sender_name=message['Username']
            ))

    def update_channel_on_message(self, channel_id: int, message: str, client_id: int):
    
        #Gets user ID
        user_id = self.client_id_user_id_map[client_id]
        #Updates database
        self.dal.add_message(channel_id, message, user_id)

        sender_data = self.dal.get_user_data(user_id)[0]
        
        #Gets channel users from database
        users = self.dal.get_channel_users(channel_id)
        for user in users:
            #Determine who needs to be notified about the message
            if user['UserID'] != user_id:
                #Checking if the user is currently still connected
                if user['UserID'] in self.user_id_client_id_map: 
                    self.add_message_by_id(self.user_id_client_id_map[user['UserID']], NewMessageNotif(
                        time_sent=datetime.now(),
                        channel_id=channel_id,
                        content=message,
                        sender_name=sender_data['Username']
                    ))


    #Updates the user on the names of the members of the channel
    def update_user_on_channel_members(self, client_id: int, channel_id: int):
        user_id = self.client_id_user_id_map[client_id]
        
        for user in self.dal.get_channel_users(channel_id):
            if user['UserID'] != user_id:
                self.add_message_by_id(client_id, UserJoinNotif(channel_id, user['Username']))

    #Updates the other uses in a channel when a user joins
    def update_users_on_user_join(self, client_id: int, channel_id: int):

        user_id = self.client_id_user_id_map[client_id]
        
        username = self.dal.get_user_data(user_id)[0]['Username']

        for user in self.dal.get_channel_users(channel_id):
            if user['UserID'] != user_id:
                #If the user needed to be updated is currently online
                if user['UserID'] in self.user_id_client_id_map:
                    #Maps user id to client id to be able to send message
                    self.add_message_by_id(self.user_id_client_id_map[user['UserID']], UserJoinNotif(channel_id, username))


    #Updates clients after login on everything 
    def update_client(self, client_id: int):

        user_id = self.client_id_user_id_map[client_id]
        for channel in self.dal.get_user_channels(user_id):

            channel_id = channel['ChannelID']
            self.add_message_by_id(client_id, ChannelJoinResponse(
                success = True,
                channel_id = channel_id,
                channel_name = channel['ChannelName']
            ))

            self.update_user_on_channel_messages(client_id, channel_id)
            self.update_user_on_channel_members(client_id, channel_id)


    # //// General Handler ////

    def handle_message(self, msg: TCPMessage, client_id):
        
        if isinstance(msg, TextMessage):
            
            self.update_channel_on_message(msg.channel_id, msg.content, client_id)

        elif isinstance(msg, ConnectionClosed):
            pass
        
        elif isinstance(msg, LoginAttempt):
            user_id = self.dal.get_user_id(msg.username)            
            if user_id == None:
                self.add_message_by_id(client_id, LoginResponse(
                    ip=0,
                    success=False,
                    user_id = user_id
                ))
            else:
                #save the client_id -> user_id mapping
                self.client_id_user_id_map[client_id] = user_id
                self.user_id_client_id_map[user_id] = client_id

                self.add_message_by_id(client_id, LoginResponse(
                    ip=0,
                    user_id= user_id,
                    success=True
                ))
                self.update_client(client_id)


        elif isinstance(msg, ChannelLeave):
            user_id = self.client_id_user_id_map[client_id]
            print(msg.channel_id, user_id)
            self.dal.remove_user_from_channel(msg.channel_id, user_id)
            
            for member in self.dal.get_channel_users(msg.channel_id):
                channel_member_id = member['UserID']
                if channel_member_id in self.user_id_client_id_map:
                    client_id = self.user_id_client_id_map[channel_member_id]
                    self.add_message_by_id(client_id, UserLeaveNotification(msg.channel_id, user_id))


        elif isinstance(msg, ChannelJoinRequest):
            user_id = self.client_id_user_id_map[client_id]
            #TODO: check if channel exists
            self.dal.add_user_channel_connection(msg.channel_id, user_id)
            channel_data = self.dal.get_channel_data(msg.channel_id)[0]
            self.add_message_by_id(client_id, ChannelJoinResponse(
                success = True,
                channel_id = msg.channel_id,
                channel_name= channel_data['ChannelName']
            ))
            self.update_user_on_channel_messages(client_id, msg.channel_id)

            self.update_users_on_user_join(client_id, msg.channel_id)
            self.update_user_on_channel_members(client_id, msg.channel_id)

        elif isinstance(msg, ChannelCreateRequest):
            
            user_id = self.client_id_user_id_map[client_id]

            channel_id = self.dal.add_channel(msg.channel_name, user_id)
            self.dal.add_user_channel_connection(channel_id, user_id)
            channel_data = self.dal.get_channel_data(channel_id)[0]

            self.add_message_by_id(client_id, ChannelCreateResponse(
                success=True,
                channel_id=channel_id,
                channel_name= channel_data['ChannelName']
            ))

        elif isinstance(msg, SearchRequest):
            RESPONSE_LIMIT = 10
            user_id = self.client_id_user_id_map[client_id]
            responses = self.dal.search_request(user_id, msg.content)[:RESPONSE_LIMIT]
            
            for response in responses:
                response_user_id = response.pop('UserID', None)
                    
                account_created_date = response.pop("DateAccountCreated", None)
                account_age = relativedelta(datetime.now(), account_created_date)

                if account_age.hours:
                    account_age_formatted = f"Account created: {account_age.hours} hours, and {account_age.minutes} minutes ago"
                elif account_age.minutes:
                    account_age_formatted = f"Account created: {account_age.minutes} minutes, and {account_age.seconds} seconds ago"
                else:
                    account_age_formatted = f"Account created: {account_age.seconds} seconds ago"

                response["AccountAge"] = account_age_formatted

            self.add_message_by_id(client_id, SearchReponse(
                response_data = responses
            ))