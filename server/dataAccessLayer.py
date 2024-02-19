from datetime import datetime
from math import tanh
import os

from bcryptCPP import bcrypt, generate_random_salt
from database.mySQLInterface import MySQLConnection
from database.graphDBInterface import GraphDBConnection
from database.region import Region
from database.databaseReset import reset_database
from database.databaseMockDataFill import fill_data
from typing import Union

class DataAccessLayer:
    def __init__(self, db_name, gdb_name) -> None:
        self.db_name = db_name
        self.gdb_name = gdb_name
        
   
    def add_user(self, username: str, firstname: str, lastname: str, email: str, password: str, dob: datetime):
        with MySQLConnection(self.db_name) as db:
            pepper = os.environ.get("SocioXPepper", "")
            salt = generate_random_salt() 

            password_hash = bcrypt(password + pepper, salt, 8)
            db.add_user(username, firstname, lastname, email, password_hash, salt, Region.EUROPE, dob)
        with GraphDBConnection(self.gdb_name) as gdb:
            gdb.addUser(username)

    def verify_password(self, user_id: str, password: str) -> bool:
        with MySQLConnection(self.db_name) as db:
            pepper = os.environ.get("SocioXPepper", "") 
            salt = db.get_user_salt(user_id)
            password_hash = bcrypt(password + pepper, salt, 8)
            return db.get_user_password_hash(user_id) == password_hash

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

    def get_user_id_from_username(self, username: str) -> Union[int, None]:
        with MySQLConnection(self.db_name) as db:
            result = db.get_user_id_from_username(username)
            if result:
                return result[0]['UserID']
    
    def get_user_id_from_email(self, email: str) -> Union[int, None]:
        with MySQLConnection(self.db_name) as db:
            result = db.get_user_id_from_email(email)
            if result:
                return result[0]['UserID']

    def get_channels_messages(self, channel_id: int):
        with MySQLConnection(self.db_name) as db:
            return db.get_channels_messages(channel_id)
    
    def remove_user_from_channel(self, channel_id: int, user_id: int):
        with MySQLConnection(self.db_name) as db:
            db.remove_user_from_channel(channel_id, user_id)
        self.recalculate_weight(user_id)


    def get_user_suggestions(self, username: str, friends: set[str]):
        with GraphDBConnection(self.gdb_name) as gdb:
            return gdb.getUserSuggestion(username, friends)


    def search_request(self, user_id: int, content: str):
        with MySQLConnection(self.db_name) as db:
            return db.search_by_prefix(user_id, content)

    def add_friend_request(self, sender_id: int, receiver_id: int):
        with MySQLConnection(self.db_name) as db:
            db.add_friend_request(sender_id, receiver_id)
        self.recalculate_weight(sender_id)
        self.recalculate_weight(receiver_id)
        

    def accept_friend_request(self, sender_id: int, receiver_id: int):
        with MySQLConnection(self.db_name) as db:
            db.accept_friend_request(sender_id, receiver_id)
        self.recalculate_weight(sender_id)
        self.recalculate_weight(receiver_id)

    def reject_friend_request(self, sender_id: int, receiver_id: int):
        with MySQLConnection(self.db_name) as db:
            db.reject_friend_request(sender_id, receiver_id)
        self.recalculate_weight(sender_id)
        self.recalculate_weight(receiver_id)

    #Returns outgoing and incoming friend requests even uncompleted ones
    def get_user_friend_connections(self, user_id):
        with MySQLConnection(self.db_name) as db:
            return db.get_user_friend_connections(user_id)
        
    #Returns only accepted friend requests
    def get_user_friends(self, user_id):
        with MySQLConnection(self.db_name) as db:
            return db.get_user_friends(user_id)
    
    def remove_friend(self, user_id_1: int, user_id_2: int):
        with MySQLConnection(self.db_name) as db:
            db.remove_friend(user_id_1, user_id_2)
        self.recalculate_weight(user_id_1)
        self.recalculate_weight(user_id_2)

    def reset_db(self):
        reset_database(self.db_name, self.gdb_name)

    def fill_with_mock_data(self):
        fill_data(self.db_name, self.gdb_name)

    def recalculate_weight(self, user_id: int):
        
        with MySQLConnection(self.db_name) as db:
            username = db.get_user_data(user_id)[0]['Username']

            #Get users channels
            channel_ids = [c["ChannelID"] for c in db.get_users_channels(user_id)]

            #2 users are connected if they share channel or are friends
            connected_users = set()

            #Get user's connected users
            for channel_id in channel_ids:
                for user in db.get_channel_users(channel_id):
                    connection_user_id =  user["UserID"]
                    connection_username = user["Username"]
                    connected_users.add((connection_user_id, connection_username))

            if (user_id, username) in connected_users:
                connected_users.remove((user_id, username))

            
            #Get users friends and adjoin them to connected users
            outgoing, incoming = db.get_user_friend_connections(user_id)
            friends = set([(f["UserID"], f["Username"]) for f in db.get_user_friends(user_id)])

            num_friends = len(friends)
            connected_users = connected_users.union(friends)

            connected_users = list(connected_users)

            FRIEND_POINTS_MAX = 10
            CHANNEL_POINTS_MAX = 10
            MESSAGE_POINTS_MAX = 10

            MAX_POINTS = FRIEND_POINTS_MAX + CHANNEL_POINTS_MAX + MESSAGE_POINTS_MAX

            weights = []
            for conn_user_id, conn_username in connected_users:
                points = 0

                #1. Calculating proportion of common channels against total channels
                #Get channels of connected user
                conn_channel_ids = set([c["ChannelID"] for c in db.get_users_channels(conn_user_id)])
                #Get common channels
                common_channels = set(channel_ids).intersection(set(conn_channel_ids))
                if len(channel_ids) != 0:
                    points += (len(common_channels)/ len(channel_ids)) * CHANNEL_POINTS_MAX


                #2. Calculating proportion of common friends against total friends
                #Get friends of connected user
                conn_friends = [(f["UserID"], f["Username"]) for f in db.get_user_friends(conn_user_id)]
                #Get common friends
                common_friends = friends.intersection(set(conn_friends))
                if num_friends != 0:
                    points += (len(common_friends)/ num_friends) * FRIEND_POINTS_MAX

                #3. Calculating proportion of messaged exchanged against total messages
                points += db.get_proption_of_messages_exchanged(user_id, conn_user_id) * MESSAGE_POINTS_MAX
                #Apply inverting and normalising function
                
                
                weight = MAX_POINTS * (1-tanh(points/MAX_POINTS))
                weights.append((conn_username, weight))

            with GraphDBConnection(self.gdb_name) as gdb:

                for conn_username, weight in weights:
                    gdb.addEdge(username, conn_username, weight)

                       

    def add_email_code(self, email: str, code: str, user_id: Union[int, None] = None):
        with MySQLConnection(self.db_name) as db:
            db.add_email_code(email, code, user_id)

    def get_most_recent_email_code(self, email: str) -> str:
        with MySQLConnection(self.db_name) as db:
            return db.get_most_recent_email_code(email)