from datetime import datetime
from mySQLInterface import MySQLConnection
from random import randint
from region import Region


with MySQLConnection('chatapp') as db:
    """
    db.add_user(
        username = "1",
        firstname= "Alex",
        lastname= "Davicenko",
        email="adavicenko@gmail.com",
        region= Region.AFRICA,
        date_of_birth=datetime(2006, 3, 3)
    )
    db.add_user(
        username = "1",
        firstname= "Alex",
        lastname= "Davicenko",
        email="adavicenkomail.com",
        region= Region.AFRICA,
        date_of_birth=datetime(2006, 3, 3)
    )
    db.add_channel(
        channel_name= "MyFirstChannel",
        owner_id= 5
    )
    """
    
    #db.add_user_channel_connection(2, 4)

    data = db.read_table("Channels")

    print()

    for row in data:
        print(row)

    data = db.read_table("UserChannelConnection")

    print()
    for row in data:
        print(row)

    data = db.get_users_channels(4)
    print()
    for row in data:
        print(row)