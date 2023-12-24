#https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html

import os
import logging

import mysql.connector
import mysql.connector.errorcode

from typing import TypeVar, List, Dict, Any
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

    def add_user(self, username: str, firstname: str, lastname: str, email: str, region: Region, date_of_birth: datetime):
        self.__execute_query(
            f"""
            INSERT INTO Users (Username, Firstname, Lastname, Email, Region, DateOfBirth, DateAccountCreated)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, username, firstname, lastname, email, region.name, self.convert_datetime_format(date_of_birth), self.convert_datetime_format(datetime.now())
        )

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
    
    def get_user(self, username) -> List[Dict[str, Any]]:
        return self.__execute_query(
            f"""
            SELECT UserID 
            FROM users 
            WHERE username = %s;
            """, username
        )
    
    def get_user_data(self, user_id) -> List[Dict[str, Any]]:
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


    def get_channel_users(self, channel_id) -> List[Dict[str, Any]]:
        return self.__execute_query(
            f"""
            SELECT u.UserID, u.Username FROM UserChannelConnection as uc
            LEFT JOIN Users as u
            ON u.UserID = uc.UserID
            WHERE uc.ChannelID = %s
            """, channel_id
        )

    def get_users_channels(self, user_id) -> List[Dict[str, Any]]:
        return self.__execute_query(
            f"""
            SELECT c.ChannelID, c.ChannelName FROM UserChannelConnection as uc
            LEFT JOIN Channels as c
            ON c.ChannelID = uc.ChannelID
            WHERE uc.UserID = %s
            """, user_id
        )
    
    def get_channels_messages(self, channel_id: int):
        return self.__execute_query(
            """
            SELECT m.MessageID, m.DateSent, m.Content, u.Username FROM messages as m
            INNER JOIN users as u
            ON u.UserID = m.SenderID 
            WHERE m.ChannelID = %s
            ORDER BY m.DateSent ASC
            """, channel_id
        )
    
    def remove_user_from_channel(self, channel_id: int, user_id: int):
        self.__execute_query(
            """
            DELETE FROM userchannelconnection as ucc
            WHERE ucc.UserID = %s
            AND ucc.ChannelID = %s
            """, user_id, channel_id
            )
    
    def search_by_prefix(self, user_id, prefix: str) -> List[Dict[str, Any]]:
        search_term = f"%{prefix.lower()}%"

        return self.__execute_query(
            """
            SELECT UserID, Username, Firstname, Region, DateAccountCreated
            FROM Users
            WHERE UserID != %s
            AND (LOWER(Firstname) LIKE %s
            OR LOWER(Username) LIKE %s
            )
            """, user_id, search_term, search_term, search_term
            )      

    def read_table(self, table_name):
        return self.__execute_query(f""" SELECT * FROM {table_name}""")


    def __execute_query(self, query: str, *args) -> List[Dict[str, Any]]:
        try:
            self.cursor.execute(query, args)
            data = self.cursor.fetchall()
            self.cnx.commit()

            if data:
                column_names = [i[0] for i in self.cursor.description]
                return [dict(zip(column_names, row)) for row in data]
            
        except mysql.connector.Error as err:
            print(f"An error has occoured: {err}")

        return []