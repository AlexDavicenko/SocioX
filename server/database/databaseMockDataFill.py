from datetime import datetime
from dateutil.relativedelta import relativedelta
import os

from database.mySQLInterface import MySQLConnection
from database.graphDBInterface import GraphDBConnection
from database.region import Region
from bcryptCPP import bcrypt, generate_random_salt

def fill_data(db_name, gdb_name):
    usernames = []
    with MySQLConnection(db_name) as db:
        regions = [Region.AFRICA, Region.ASIA, Region.EUROPE, Region.NORTH_AMERICA, Region.SOUTH_AMERICA]
        with open("database/mockDBdata.txt", "r") as f:
            mock_data = f.read().splitlines()
            for i in range(len(mock_data)):
                salt = generate_random_salt()
                firstname, lastname = mock_data[i].split(" ")
                db.add_user(
                    username= firstname.lower()+str(i), #Ensure unique
                    firstname= firstname,
                    lastname= lastname,
                    email= f"{firstname}.{lastname}@gmail.com",
                    password_hash= bcrypt("pass"+os.environ.get("SocioXPepper", ""), salt, 8),
                    password_salt= salt,
                    region=regions[i%5],
                    date_of_birth=datetime(1990,1,1) + relativedelta(year = i//12, month=(i%12)+1,day=7) # Random looking consistent birthdays
                )                
                usernames.append(firstname.lower()+str(i))


                
        db.add_channel(
        channel_name="Sports",
        owner_id=1,
        created_datetime=datetime.now()
        )
        db.add_user_channel_connection(1, 1)

        db.add_channel(
            channel_name="Music",
            owner_id=1,
            created_datetime=datetime.now()
        )
        db.add_user_channel_connection(2, 1)

        db.add_channel(
            channel_name="Movies",
            owner_id=2,
            created_datetime=datetime.now()
        )
        db.add_user_channel_connection(3, 2)

        db.add_channel(
            channel_name="Food",
            owner_id=2,
            created_datetime=datetime.now()
        )
        db.add_user_channel_connection(4, 2)

        db.add_channel(
            channel_name="Travel",
            owner_id=2,
            created_datetime=datetime.now()
        )
        db.add_user_channel_connection(5, 2)

        db.add_channel(
            channel_name="Books",
            owner_id=2,
            created_datetime=datetime.now()
        )
        db.add_user_channel_connection(6, 2)

        db.add_channel(
            channel_name="Technology",
            owner_id=3,
            created_datetime=datetime.now()
        )
        db.add_user_channel_connection(7, 3)

        db.add_channel(
            channel_name="Health",
            owner_id=3,
            created_datetime=datetime.now()
        )
        db.add_user_channel_connection(8, 3)

        db.add_channel(
            channel_name="Fashion",
            owner_id=3,
            created_datetime=datetime.now()
        )
        db.add_user_channel_connection(9, 3)

        db.add_channel(
            channel_name="Art",
            owner_id=4,
            created_datetime=datetime.now()
        )
        db.add_user_channel_connection(10, 4)

    try:
        #TODO: DO NOT ALLOW COMMAS OR ANY SPECIAL CHARS IN THE USERNAME (USE REGEX TO VERIFY USER INPUT)
        with GraphDBConnection(gdb_name) as gdb:
            for username in usernames:
                gdb.addUser(username)
            

    except Exception as e:
        print(e)
