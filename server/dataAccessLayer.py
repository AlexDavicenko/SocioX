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
        self.graph_db = Graph()
        
   

    def add_user(self, username) -> None:
        with MySQLConnection(self.db_name) as db:
            db.add_user(username, "TEST", "TEST", "TEST", Region.EUROPE, datetime.now())
        with GraphDBConnection(self.db_name) as gdb:
            gdb.addUser(username)


    def add_channel(self, channel_name: str, owner_id: int) -> int:
        with MySQLConnection(self.db_name) as db:
            dt = datetime.now()
            db.add_channel(channel_name, owner_id, dt)
            return db.get_channel_id(channel_name, owner_id, dt)[0]['ChannelID']

    def add_user_channel_connection(self, channel_id: int, user_id: int):
        with MySQLConnection(self.db_name) as db:
            db.add_user_channel_connection(channel_id, user_id)

    def add_message(self, channel_id: int, content: str, user_id: int):
        with MySQLConnection(self.db_name) as db:
            db.add_message(channel_id, content, user_id)

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
            result = db.get_user(username)
            if result:
                return result[0]['UserID']
    
    def get_channels_messages(self, channel_id: int):
        with MySQLConnection(self.db_name) as db:
            return db.get_channels_messages(channel_id)
    
    def remove_user_from_channel(self, channel_id: int, user_id: int):
        with MySQLConnection(self.db_name) as db:
            return db.remove_user_from_channel(channel_id, user_id)

    def get_user_suggestions(self, user_id):
        
        #TODO
        pass 

    def search_request(self,user_id, content):
        with MySQLConnection(self.db_name) as db:
            return db.search_by_prefix(user_id, content)

    def reset_db(self):
        reset_database(self.db_name, self.gdb_name)

    def fill_with_mock_data(self):
        fill_data(self.db_name, self.gdb_name)

