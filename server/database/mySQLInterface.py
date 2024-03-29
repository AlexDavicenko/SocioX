import os

import mysql.connector
import mysql.connector.errorcode

from typing import TypeVar, List, Dict, Any, Tuple, Union
from types import TracebackType
from datetime import datetime

from database.region import Region


T = TypeVar('T', bound = 'MySQLConnection')

class MySQLConnection:
    DB_NAME: str

    def __init__(self, database_name: str) -> None:
        self.DB_NAME = database_name

    def __enter__(self: T) -> T:
        self.cnx = mysql.connector.connect(host = "localhost", user = 'root', password = os.getenv('MySQLPassword'))
        self.cursor = self.cnx.cursor(buffered=False)
        self.connect_to_database()
        return self 
    
    def __exit__(self, exc_type: type[BaseException], exc_value: BaseException, trackeback: TracebackType) -> None:
        self.cursor.close()
        self.cnx.close()


    def create_database(self) ->  None:
        try:
            self.cursor.execute(f"CREATE DATABASE {self.DB_NAME} DEFAULT CHARACTER SET 'utf8'")
        except mysql.connector.Error as err:
            print(f"Failed creating database: {err}")
        self.connect_to_database()

    
    def connect_to_database(self) -> None:
        try:
            self.cursor.execute(f"USE {self.DB_NAME}")
        except mysql.connector.Error as err:
            print(f"Database {self.DB_NAME} does not exists.")

    def convert_datetime_format(self, datetimeObj: datetime):
        return datetimeObj.strftime(r'%Y-%m-%d %H:%M:%S')

    def delete_database(self) -> None:
        self.__execute_query(f"""DROP DATABASE {self.DB_NAME}""")
    
    def create_table(self, table_name: str, table_description: str) -> None:
        print(f"Creating table {table_name}")
        self.__execute_query(table_description)

    def add_user(
            self, 
            username: str, 
            firstname: str, 
            lastname: str, 
            email: str, 
            password_hash: str, 
            salt: str, 
            region: Region, 
            date_of_birth: datetime):
        self.__execute_query(
            f"""
            INSERT INTO Users 
            (Username, Firstname, Lastname, Email, PasswordHash, PasswordSalt, Region, DateOfBirth, DateAccountCreated)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, username,
            firstname, 
            lastname, 
            email, 
            password_hash, 
            salt, 
            region.name, 
            self.convert_datetime_format(date_of_birth), 
            self.convert_datetime_format(datetime.now())
        )

    def get_user_salt(self, user_id: str) -> str:
        return self.__execute_query(
            f"""
            SELECT PasswordSalt 
            FROM users 
            WHERE UserID = %s;
            """, user_id
        )[0]["PasswordSalt"]

    def get_user_password_hash(self, user_id: str) -> str:
        return self.__execute_query(
            f"""
            SELECT PasswordHash 
            FROM users 
            WHERE UserID = %s;
            """, user_id
        )[0]["PasswordHash"]


    def add_channel(self, channel_name: str, owner_id: int, created_datetime: datetime):
        self.__execute_query(
            f"""
            INSERT INTO Channels (ChannelName, DateCreated, OwnerID)
            VALUES (%s, %s, %s)
            """, channel_name, self.convert_datetime_format(created_datetime), owner_id
        )
    
    def get_channel_id(self, channel_name: str, owner_id: int, created_datetime: datetime) -> List[Dict[str, Any]]:
        return self.__execute_query(
            f"""
            SELECT ChannelID 
            FROM channels
            WHERE ChannelName = %s AND DateCreated = %s AND OwnerID = %s;
            """, channel_name, self.convert_datetime_format(created_datetime), owner_id
        )
    
    def get_user_id_from_username(self, username: str) -> List[Dict[str, Any]]:
        return self.__execute_query(
            f"""
            SELECT UserID 
            FROM users 
            WHERE username = %s;
            """, username
        )

    def get_user_id_from_email(self, email: str) -> List[Dict[str, Any]]:
        return self.__execute_query(
            f"""
            SELECT UserID 
            FROM users 
            WHERE email = %s;
            """, email
        )
    
    def get_user_data(self, user_id: int) -> List[Dict[str, Any]]:
        return self.__execute_query(
            f"""
            SELECT *
            FROM users 
            WHERE UserID = %s;
            """, user_id
        )
    def get_channel_data(self, channel_id) -> List[Dict[str, Any]]:
        return self.__execute_query(
            f"""
            SELECT *
            FROM channels 
            WHERE ChannelID = %s;
            """, channel_id
        )


    def add_user_channel_connection(self, channel_id: int, user_id: int):
        self.__execute_query(
            f"""
            INSERT INTO UserChannelConnection (ChannelID, DateUserAdded, UserID)
            VALUES (%s, %s, %s)
            """, channel_id, self.convert_datetime_format(datetime.now()), user_id
        )

    def add_message(self, channel_id: int, content: str, sender_id: int):
        self.__execute_query(
            f"""
            INSERT INTO Messages (ChannelID, Content, DateSent, SenderID)
            VALUES (%s, %s, %s, %s)
            """, channel_id, content, self.convert_datetime_format(datetime.now()), sender_id
        )


    def get_channel_users(self, channel_id: int) -> List[Dict[str, Any]]:
        return self.__execute_query(
            f"""
            SELECT u.UserID, u.Username, u.Firstname, u.Lastname FROM UserChannelConnection AS uc
            LEFT JOIN Users AS u
            ON u.UserID = uc.UserID
            WHERE uc.ChannelID = %s
            """, channel_id
        )

    def get_users_channels(self, user_id) -> List[Dict[str, Any]]:
        return self.__execute_query(
            f"""
            SELECT c.ChannelID, c.ChannelName FROM UserChannelConnection AS uc
            LEFT JOIN Channels AS c
            ON c.ChannelID = uc.ChannelID
            WHERE uc.UserID = %s
            """, user_id
        )
    
    def get_channels_messages(self, channel_id: int):
        return self.__execute_query(
            """
            SELECT m.MessageID, m.DateSent, m.Content, u.Username FROM messages AS m
            INNER JOIN users AS u
            ON u.UserID = m.SenderID 
            WHERE m.ChannelID = %s
            ORDER BY m.DateSent ASC
            """, channel_id
        )
    
    def remove_user_from_channel(self, channel_id: int, user_id: int):
        self.__execute_query(
            """
            DELETE FROM userchannelconnection AS ucc
            WHERE ucc.UserID = %s
            AND ucc.ChannelID = %s
            """, user_id, channel_id
            )
    
    def search_by_prefix(self, user_id, prefix: str) -> List[Dict[str, Any]]:
        search_term = f"%{prefix.lower()}%"

        return self.__execute_query(
            """
            SELECT UserID, Username, Firstname, Lastname, Region, DateAccountCreated
            FROM Users
            WHERE UserID != %s
            AND (LOWER(Firstname) LIKE %s
            OR LOWER(Username) LIKE %s
            OR LOWER(Lastname) LIKE %s
            )
            """, user_id, search_term, search_term, search_term
            )      
    
    def add_friend_request(self, sender_id: int, receiver_id: int):
        self.__execute_query(
            """
            INSERT INTO FriendConnections (FriendRequestSenderID, FriendRequestReceiverID, Accepted)
            VALUES (%s, %s, False)
            """, sender_id, receiver_id
            )
        
    def accept_friend_request(self, sender_id: int, receiver_id: int):
        self.__execute_query("""
            UPDATE FriendConnections
            SET Accepted = True, DateRequestAccepted = %s
            WHERE FriendRequestSenderID = %s
            AND FriendRequestReceiverID = %s
            """, self.convert_datetime_format(datetime.now()), sender_id, receiver_id)

    def reject_friend_request(self, sender_id: int, receiver_id: int):
        self.__execute_query("""
            DELETE FROM FriendConnections
            WHERE FriendRequestSenderID = %s
            AND FriendRequestReceiverID = %s
            """, sender_id, receiver_id)
    
    def remove_friend(self, user_id_1: int, user_id_2: int):
        self.__execute_query("""
            DELETE FROM FriendConnections
            WHERE (FriendRequestSenderID = %s
            AND FriendRequestReceiverID = %s)
            OR (FriendRequestSenderID = %s
            AND FriendRequestReceiverID = %s)
            """, user_id_1, user_id_2, user_id_2, user_id_1)

    #Returns outgoing and incoming friend requests even uncompleted ones
    def get_user_friend_connections(self, user_id: int) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        #All outgoing friend requests
        return self.__execute_query(
            """
            SELECT u.UserID, u.Username, u.Firstname, u.Lastname, fc.FriendRequestReceiverID, fc.Accepted, fc.DateRequestAccepted
            FROM FriendConnections AS fc, Users AS u
            WHERE fc.FriendRequestSenderID = %s
            AND fc.FriendRequestReceiverID = u.UserID            
            """, user_id
        #All incoming friend requests
        ), self.__execute_query(
            """
            SELECT u.UserID, u.Username, u.Firstname, u.Lastname, fc.FriendRequestSenderID, fc.Accepted, fc.DateRequestAccepted
            FROM FriendConnections AS fc, Users AS u
            WHERE fc.FriendRequestReceiverID = %s
            AND fc.FriendRequestSenderID = u.UserID    
            """, user_id
        )
    #Returns only accepted friend requests
    def get_user_friends(self, user_id: int) -> List[Dict[str, Any]]:
        return self.__execute_query(
            """
            SELECT u.UserID, u.Username, u.Firstname, u.Lastname, fc.DateRequestAccepted
            FROM FriendConnections AS fc, Users AS u
            WHERE (fc.FriendRequestSenderID = %s OR fc.FriendRequestReceiverID = %s)
            AND (u.UserID = fc.FriendRequestSenderID OR u.UserID = fc.FriendRequestReceiverID)
            AND fc.Accepted = True
            """, user_id, user_id
        )
    
    def get_proption_of_messages_exchanged(self, user_id: int, conn_user_id: int) -> float:
        return float(self.__execute_query(
            #Messages sent by user in channels where connected user is also a member / all messages sent by user  
            """
            SELECT 
                CASE 
                    WHEN (allMessages = 0) THEN 0
                    ELSE exchangedMessages/allMessages 
                END AS Proportion 
            FROM(
                    SELECT COUNT(*) AS exchangedMessages
                    FROM Messages AS m
                    WHERE (m.SenderID = %s AND m.ChannelID IN (
                        SELECT uc.ChannelID
                        FROM UserChannelConnection AS uc
                        WHERE uc.UserID = %s
                    ))
                ) exchangedMessagesCount, 
                (
                    SELECT COUNT(*) AS allMessages
                    FROM Messages AS m 
                    WHERE m.SenderID = %s
                ) allMessagesCount
            """, user_id, conn_user_id, user_id
        )[0]['Proportion'])
    
    def add_email_code(self, email: str, code: str, user_id: Union[int, None] = None):
        if user_id: # I am so glad UserIDs do not start at 0 in MySQL<3
            self.__execute_query(
                """
                INSERT INTO EmailCodes (Email, Code, DateCodeSent, UserID)
                VALUES (%s, %s, %s)
                """, email, code, self.convert_datetime_format(datetime.now()), user_id
            )
        else:
            self.__execute_query(
                """
                INSERT INTO EmailCodes (Email, Code, DateCodeSent)
                VALUES (%s, %s, %s)
                """, email, code, self.convert_datetime_format(datetime.now())
            )

    def get_most_recent_email_code(self, email: str) -> str:
        return self.__execute_query(
            """
            SELECT Code
            FROM EmailCodes
            WHERE Email = %s
            ORDER BY DateCodeSent DESC
            LIMIT 1
            """, email
        )[0]["Code"]

    def read_table(self, table_name):
        return self.__execute_query(f""" SELECT * FROM {table_name}""")


    def __execute_query(self, query: str, *args) -> List[Dict[str, Any]]:
        try:
            self.cursor.execute(query, args)
            data = self.cursor.fetchall()
            self.cnx.commit()

            if data:
                column_names = [column[0] for column in self.cursor.description]
                return [dict(zip(column_names, row)) for row in data]
            
        except mysql.connector.Error as err:
            print(f"An error has occoured: {err}")

        return []