from datetime import datetime

from database.mySQLInterface import MySQLConnection
from database.region import Region

from typing import Union

class DataAccessLayer:
    def __init__(self, db_name) -> None:
        self.db_name = db_name
   

    def add_user(self, username) -> None:
        with MySQLConnection(self.db_name) as db:
            db.add_user(username, "TEST", "TEST", "TEST", Region.EUROPE, datetime.now())
        
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

if __name__ == '__main__':
        
    dal = DataAccessLayer('chatapp')

    dal.add_user("User1")
    dal.add_user("User2")
    dal.add_user("User3")
    dal.add_user("User4")

    #user2_id = dal.get_user_id('User2')
    #user3_id = dal.get_user_id('User3')
    
    #print(user2_id)
    #channel1_id = dal.add_channel('Channel1', user2_id)
    #channel1_id = 3
    #print(channel1_id)
    
    #dal.add_user_channel_connection(channel1_id, user2_id)
    #dal.add_user_channel_connection(channel1_id, user3_id)

    

    #print(dal.get_channel_users(channel1_id))
    
    #dal.get_user_channels(0)
