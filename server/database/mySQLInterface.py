#https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html

import mysql.connector
import mysql.connector.errorcode

from typing import TypeVar
from types import TracebackType
import os



T = TypeVar('T', bound = 'MySQLConnection')

class MySQLConnection:
    DB_NAME: str

    def __init__(self, database_name: str) -> None:
        self.DB_NAME = database_name

    def __enter__(self: T) -> T:
        self.cnx = mysql.connector.connect(user = 'root', password = os.getenv('MySQLPassword'))
        self.cursor = self.cnx.cursor()
        self.connect_to_database()
        return self
    
    def __exit__(self, exc_type: type[BaseException], exc_value: BaseException, trackeback: TracebackType) -> None:
        
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

    def delete_database(self) -> None:
        self.__execute_query(f"""DROP DATABASE {self.DB_NAME}""")
    
    def create_table(self, table_name: str, table_description: str) -> None:
        print(f"Creating table {table_name}")
        self.__execute_query(table_description)

    def __execute_query(self, query: str) -> None:
        try:
            self.cursor.execute(query)
        except mysql.connector.Error as err:
            print(err)

    