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

    def save_client_user_id_mapping(self, client_id: int , user_id: int):
        self.client_id_user_id_map[client_id] = user_id
        self.user_id_client_id_map[user_id] = client_id

    @staticmethod
    def format_age(start: datetime) -> str:

        account_age = relativedelta(datetime.now(), start)

        if account_age.hours:
            age_formatted = f"{account_age.hours} hours, and {account_age.minutes} minutes ago"
        elif account_age.minutes:
            age_formatted = f"{account_age.minutes} minutes, and {account_age.seconds} seconds ago"
        else:
            age_formatted = f"{account_age.seconds} seconds ago"
        return age_formatted

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

    def update_channel_on_message(self, channel_id: int, message: str, user_id: int):
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
                self.add_message_by_id(client_id, UserJoinNotif(channel_id, user['Username'], user['Firstname'], user['Lastname']))

    #Updates the other uses in a channel when a user joins
    def update_users_on_user_join(self, client_id: int, channel_id: int):

        user_id = self.client_id_user_id_map[client_id]
        
        user_data = self.dal.get_user_data(user_id)[0]

        username = user_data['Username']
        firstname = user_data['Firstname']
        lastname = user_data['Lastname']

        for user in self.dal.get_channel_users(channel_id):
            if user['UserID'] != user_id:
                #If the user needed to be updated is currently online
                if user['UserID'] in self.user_id_client_id_map:
                    #Maps user id to client id to be able to send message
                    self.add_message_by_id(self.user_id_client_id_map[user['UserID']], UserJoinNotif(channel_id, username, firstname, lastname))

    def update_user_on_friend_status(self, client_id: int, user_id: int):

        connections = self.dal.get_user_friend_connections(user_id)
        if connections == ([], []):
            return
        
        outgoing_reqs, incoming_reqs = connections
        for request in outgoing_reqs:
            if request['Accepted']:
                self.add_message_by_id(client_id, FriendStatusNotif(
                    username = request['Username'],
                    firstname= request['Firstname'],
                    lastname= request['Lastname'],
                    decision="Remove"
                ))
            else:
                self.add_message_by_id(client_id, FriendStatusNotif(
                    username = request['Username'],
                    firstname= request['Firstname'],
                    lastname= request['Lastname'],
                    decision="Pending"
                ))
        for request in incoming_reqs:
            if request['Accepted']:
                self.add_message_by_id(client_id, FriendStatusNotif(
                    username = request['Username'],
                    firstname= request['Firstname'],
                    lastname= request['Lastname'],
                    decision="Remove"
                ))
            else:
                if request['DateRequestAccepted'] == None:
                    self.add_message_by_id(client_id, FriendStatusNotif(
                        username = request['Username'],
                        firstname= request['Firstname'],
                        lastname= request['Lastname'],
                        decision="Accept"
                    ))


    #Updates clients after login on everything 
    def update_client(self, client_id: int):
        user_id = self.client_id_user_id_map[client_id]
        self.update_user_on_friend_status(client_id, user_id)

        for channel in self.dal.get_user_channels(user_id):

            channel_id = channel['ChannelID']
            self.add_message_by_id(client_id, ChannelJoinResponse(
                success = True,
                channel_id = channel_id,
                channel_name = channel['ChannelName']
            ))

            self.update_user_on_channel_members(client_id, channel_id)
            self.update_user_on_channel_messages(client_id, channel_id)



    # //// General Handler ////

    def handle_message(self, msg: TCPMessage, client_id):
        
        match msg:
            case ConnectionClosed():
                #TODO: remove client_id from client_ids (proper termination of process)
                pass
            case LoginAttempt():
                user_id = self.dal.get_user_id(msg.username)          
                if user_id == None:
                    self.add_message_by_id(client_id, LoginResponse(
                        success=False,
                        user_id = None,
                        username = None,
                        firstname = None,
                        lastname = None,
                        email = None,
                        dob = None,
                        account_created = None
                    ))
                else:
                    self.save_client_user_id_mapping(client_id, user_id)
                    user_data = self.dal.get_user_data(user_id)[0]
                    self.add_message_by_id(client_id, LoginResponse(
                        user_id= user_id,
                        success=True,
                        username = user_data['Username'],
                        firstname = user_data['Firstname'],
                        lastname = user_data['Lastname'],
                        email = user_data['Email'],
                        dob = user_data['DateOfBirth'],
                        account_created = "Account created: " + self.format_age(user_data['DateAccountCreated'])
                    ))
                    self.update_client(client_id)
            case _:
                user_id = self.client_id_user_id_map[client_id]
                self.handle_logged_in_message(msg, client_id, user_id)

    def handle_logged_in_message(self, msg: TCPMessage, client_id: int, user_id: int):
        match msg:
            
            case TextMessage():
                self.update_channel_on_message(msg. channel_id, msg.content, user_id)
            case ChannelLeave():
                self.dal.remove_user_from_channel(msg.channel_id, user_id)
                username = self.dal.get_user_data(user_id)[0]['Username']
                for member in self.dal.get_channel_users(msg.channel_id):
                    channel_member_id = member['UserID']
                    #If other users in the channel are online they are notifed about the leave
                    if channel_member_id in self.user_id_client_id_map:
                        member_client_id = self.user_id_client_id_map[channel_member_id]
                        self.add_message_by_id(member_client_id, ChannelLeaveNotif(msg.channel_id, username))
            
            case ChannelJoinRequest():
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

            case ChannelCreateRequest():
                channel_id = self.dal.add_channel(msg.channel_name, user_id)
                self.dal.add_user_channel_connection(channel_id, user_id)
                channel_data = self.dal.get_channel_data(channel_id)[0]

                self.add_message_by_id(client_id, ChannelCreateResponse(
                    success=True,
                    channel_id=channel_id,
                    channel_name= channel_data['ChannelName']
                ))
            case SearchRequest():
                RESPONSE_LIMIT = 10
                responses = self.dal.search_request(user_id, msg.content)[:RESPONSE_LIMIT]
                
                for response in responses:
                    response_user_id = response.pop('UserID', None)
                        
                    account_created_date = response.pop("DateAccountCreated", None)

                    account_age_formatted = "Account created: " + self.format_age(account_created_date)
                    
                    response["AccountAge"] = account_age_formatted

                self.add_message_by_id(client_id, SearchReponse(
                    response_data = responses
                ))
            case SignUpAttempt():
                self.dal.add_user(
                    msg.username,
                    msg.firstname,
                    msg.lastname,
                    msg.email,
                    msg.dob
                )

                user_id = self.dal.get_user_id(msg.username)
                
                self.add_message_by_id(client_id, LoginResponse(
                    success= True,
                    user_id = user_id,
                    username = msg.username,
                    firstname = msg.firstname,
                    lastname = msg.lastname,
                    email = msg.email,
                    dob = msg.dob,
                    account_created = "Just now"
                ))     
                self.save_client_user_id_mapping(client_id, user_id)
                
            case FriendRequest():
                receiver_id = self.dal.get_user_id(msg.username)
                self.dal.add_friend_request(user_id, receiver_id)

                #Check if the receiver is online
                if receiver_id in self.user_id_client_id_map:
                    receiver_client_id = self.user_id_client_id_map[receiver_id]
                    sender_data = self.dal.get_user_data(user_id)[0]
                    self.add_message_by_id(receiver_client_id, FriendRequestNotif(
                        username = sender_data['Username'],
                        firstname= sender_data['Firstname'],
                        lastname= sender_data['Lastname']
                    ))
            case FriendRequestDecision():
                sender_id = self.dal.get_user_id(msg.username)
                if msg.success:
                    self.dal.accept_friend_request(sender_id, user_id)
                else:
                    self.dal.reject_friend_request(sender_id, user_id)

                if sender_id in self.user_id_client_id_map:
                    friend_client_id = self.user_id_client_id_map[sender_id]
                    sender_data = self.dal.get_user_data(user_id)[0]
                    #Same message as the one received
                    self.add_message_by_id(friend_client_id, FriendRequestDecision(
                        success=msg.success,
                        username = sender_data['Username'],
                    ))
            case FriendRemoval():
                other_user_id = self.dal.get_user_id(msg.username)
                self.dal.remove_friend(user_id, other_user_id)
                if other_user_id in self.user_id_client_id_map:
                    other_user_client_id = self.user_id_client_id_map[other_user_id]
                    self.add_message_by_id(other_user_client_id, FriendRemoval(
                        username = self.dal.get_user_data(user_id)[0]['Username']
                    ))
            