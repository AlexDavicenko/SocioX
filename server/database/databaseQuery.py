import sqlite3
from sqlite3 import Error, Connection
from datetime import date, time, datetime


class DatabaseQuery:
    def __init__(self, db_file_name) -> None:
        self.db_file_name = db_file_name
        try:
            self.conn = sqlite3.connect(db_file_name)
            self.cursor = self.conn.cursor()
            print(sqlite3.version)
            
        except Error as e:
            print(e)

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_file_name)
            self.cursor = self.conn.cursor()
            print(f"Using SQLite Version: {sqlite3.version}")
            return self
            
        except Error as e:
            print(e) 
            
    def __exit__(self, *args):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def execute_query(self, query, *args):
        try:
            self.cursor.execute(query, args)
            self.conn.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_query_with_fetch(self, query, *args):
        try:
            self.cursor.execute(query, args)
            print("Query executed successfully")
            return self.cursor.fetchall()
        except Error as e:
            print(f"The error '{e}' occurred")
    

    def get_datetime(self):
        now = datetime.now()
        return now.date(), now.strftime("%H:%M:%S")
    
    def add_user(self, name: str, email: str, password_hash: str, date_of_birth: date):

        date, time = self.get_datetime()

        query = f"""
        INSERT INTO Users (Username, DateAccountCreated, DateOfBirth, Email, PasswordHash)
        VALUES (?,?,?,?,?);
        """

        self.execute_query(query, name, date, date_of_birth, email, password_hash)

    def add_channel(self, owner_id: int, name: str):
        
        date, time = self.get_datetime()


        query = f"""
        INSERT INTO channels (ChannelOwnerID, ChannelName, ChannelCreatedDate, ChannelCreatedTime)
        VALUES (?,?,?,?);
        """

        self.execute_query(query, owner_id, name, date, time)

    def add_message(self, channel_id: int, sender_id: int, content: str):
        
        date, time = self.get_datetime()


        query = f"""
        INSERT INTO messages (ParentChannelID, ParentUserID, MessageContent, SentDate, SentTime)
        VALUES (?,?,?,?,?);
        """

        self.execute_query(query, channel_id, sender_id, content, date, time)


    def add_user_channel_connection(self, channel_id: int, user_id: id ):
        
        date, time = self.get_datetime()

        
        query = f"""
        INSERT INTO UserChannelConnections (UserID, ChannelID, ConnectionCreatedTime, ConnectionCreatedDate)
        VALUES (?,?,?,?);
        """
        self.execute_query(query, user_id, channel_id, time, date)


    def get_user_channels(self, user_id: int) -> list[int]:
        """Returns a list of channel IDs"""
        
        query = f"""
        SELECT Channels.ChannelID
        FROM UserChannelConnections
        JOIN Channels
        ON Channels.ChannelID = UserChannelConnections.ChannelID
        WHERE UserChannelConnections.UserID = {str(user_id)};
        """

        return self.execute_query_with_fetch(query)