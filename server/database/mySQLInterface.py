#https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html

import mysql.connector
import mysql.connector.errorcode
import os

from typing import TypeVar
from types import TracebackType
from datetime import datetime
from region import Region


T = TypeVar('T', bound = 'MySQLConnection')

class MySQLConnection:
    DB_NAME: str

    def __init__(self, database_name: str) -> None:
        self.DB_NAME = database_name

    def __enter__(self: T) -> T:
        self.cnx = mysql.connector.connect(host = "localhost", database = "chatapp", user = 'root', password = os.getenv('MySQLPassword'))
        self.cursor = self.cnx.cursor(buffered=False)
        self.connect_to_database()
        return self
    
    def __exit__(self, exc_type: type[BaseException], exc_value: BaseException, trackeback: TracebackType) -> None:
        print("DB Closed")
        self.cursor.close()
        self.cnx.close()


    def create_database(self) ->  None:
        try:
            self.cursor.execute(
                f"CREATE DATABASE {self.DB_NAME} DEFAULT CHARACTER SET 'utf8'")
        except mysql.connector.Error as err:
            print("Failed creating database: {err}")
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

    def add_channel(self, channel_name: str, owner_id: int):
        self.__execute_query(
            f"""
            INSERT INTO Channels (ChannelName, DateCreated, OwnerID)
            VALUES (%s, %s, %s)
            """, channel_name, self.convert_datetime_format(datetime.now()), owner_id
        )

    def add_user_channel_connection(self, channel_id: int, user_id: int):
        self.__execute_query(
            f"""
            INSERT INTO UserChannelConnection (ChannelID, DateUserAdded, UserID)
            VALUES (%s, %s, %s)
            """, channel_id, self.convert_datetime_format(datetime.now()), user_id
        )

    def add_messages(self, channel_id: int, content: str, sender_id: int):
        self.__execute_query(
            f"""
            INSERT INTO Messages (ChannelID, Content, DateSent, SenderID)
            VALUES (%s, %s, %s, %s)
            """, channel_id, content, self.convert_datetime_format(datetime.now()), sender_id
        )


    def get_channels_users(self, channel_id):
        result = self.__execute_query(
            f"""
            SELECT u.UserID, u.Username FROM UserChannelConnection as uc
            LEFT JOIN Users as u
            ON u.UserID = uc.UserID
            WHERE uc.ChannelID = %s
            """, channel_id
        )
        return list(map(lambda row: {
            'UserID': row[0],
            'Username': row[1],
        },result))

    def get_users_channels(self, user_id):
        result = self.__execute_query(
            f"""
            SELECT c.ChannelID, c.ChannelName FROM UserChannelConnection as uc
            LEFT JOIN Channels as c
            ON c.ChannelID = uc.ChannelID
            WHERE uc.UserID = %s
            """, user_id
        )
        return list(map(lambda row: {
            'ChannelID': row[0],
            'ChannelName': row[1],
        },result))


    def read_table(self, table_name):
        return self.__execute_query(f""" SELECT * FROM {table_name}""")


    def __execute_query(self, query: str, *args) -> list:
        try:
            self.cursor.execute(query, args)
            data = self.cursor.fetchall()
            self.cnx.commit()
            return data
        
        except mysql.connector.Error as err:
            print(f"An error has occoured: {err}")

        return []