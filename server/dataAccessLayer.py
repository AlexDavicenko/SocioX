from datetime import datetime
import logging

from database.mySQLInterface import MySQLConnection
from database.graphDBInterface import GraphDBConnection
from database.region import Region
from database.databaseReset import reset_database
from database.databaseMockDataFill import fill_data

from GraphDB import Graph

from typing import Union

class DataAccessLayer:
    def __init__(self, db_name, gdb_name) -> None:
        self.db_name = db_name
        self.gdb_name = gdb_name
    
   
    def add_user(self, username: str, firstname: str, lastname: str, email: str, date_of_birth: datetime) -> None:
        with MySQLConnection(self.db_name) as db:
            db.add_user(username, firstname, lastname, email, Region.EUROPE, date_of_birth)
        with GraphDBConnection(self.gdb_name) as gdb:
            gdb.addUser(username)


    def add_channel(self, channel_name: str, owner_id: int) -> int:
        with MySQLConnection(self.db_name) as db:
            dt = datetime.now()
            db.add_channel(channel_name, owner_id, dt)
            return db.get_channel_id(channel_name, owner_id, dt)[0]['ChannelID']

    def add_user_channel_connection(self, channel_id: int, user_id: int):
        with MySQLConnection(self.db_name) as db:
            db.add_user_channel_connection(channel_id, user_id)
        self.recalculate_weight(user_id)

    def add_message(self, channel_id: int, content: str, user_id: int):
        with MySQLConnection(self.db_name) as db:
            db.add_message(channel_id, content, user_id)
        self.recalculate_weight(user_id)


    def get_user_channels(self, user_id: int):
        with MySQLConnection(self.db_name) as db:
            return db.get_users_channels(user_id)

    def get_channel_users(self, channel_id: int):
        with MySQLConnection(self.db_name) as db:
            return db.get_channel_users(channel_id)

    def get_user_data(self, user_id: int):
        with MySQLConnection(self.db_name) as db:
            return db.get_user_data(user_id)

    def get_channel_data(self, channel_id: int):
        with MySQLConnection(self.db_name) as db:
            return db.get_channel_data(channel_id)

    def get_user_id(self, username: str) -> Union[int, None]:
        with MySQLConnection(self.db_name) as db:
            result = db.get_user_id(username)
            if result:
                return result[0]['UserID']
    
    def get_channels_messages(self, channel_id: int):
        with MySQLConnection(self.db_name) as db:
            return db.get_channels_messages(channel_id)
    
    def remove_user_from_channel(self, channel_id: int, user_id: int):
        with MySQLConnection(self.db_name) as db:
            db.remove_user_from_channel(channel_id, user_id)
        self.recalculate_weight(user_id)


    def get_user_suggestions(self, user_id):
        
        #TODO
        pass 

    def search_request(self, user_id: int, content: str):
        with MySQLConnection(self.db_name) as db:
            return db.search_by_prefix(user_id, content)

    def add_friend_request(self, sender_id: int, receiver_id: int):
        with MySQLConnection(self.db_name) as db:
            db.add_friend_request(sender_id, receiver_id)

    def accept_friend_request(self, sender_id: int, receiver_id: int):
        with MySQLConnection(self.db_name) as db:
            db.accept_friend_request(sender_id, receiver_id)
    
    def reject_friend_request(self, sender_id: int, receiver_id: int):
        with MySQLConnection(self.db_name) as db:
            db.reject_friend_request(sender_id, receiver_id)

    def get_user_friend_connections(self, user_id):
        with MySQLConnection(self.db_name) as db:
            return db.get_user_friend_connections(user_id)
    
    def remove_friend(self, user_id_1: int, user_id_2: int):
        with MySQLConnection(self.db_name) as db:
            db.remove_friend(user_id_1, user_id_2)

    def reset_db(self):
        reset_database(self.db_name, self.gdb_name)

    def fill_with_mock_data(self):
        fill_data(self.db_name, self.gdb_name)

    def recalculate_weight(self, user_id: int):
        
        with MySQLConnection(self.db_name) as db:
            username = db.get_user_data(user_id)[0]['Username']

            channel_ids = [c["ChannelID"] for c in db.get_users_channels(user_id)]

            connected_users = set()

            for channel_id in channel_ids:
                for user in db.get_channel_users(channel_id):
                    connection_user_id =  user["UserID"]
                    connection_username = user["Username"]
                    connected_users.add((connection_user_id, connection_username))

            if (user_id, username) in connected_users:
                connected_users.remove((user_id, username))

            connected_users = list(connected_users)
            
            #print(connected_users)

                       

