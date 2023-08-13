from datetime import datetime
from server.database.databaseQuery import DatabaseQuery

#https://youtu.be/wJanjCfyhAk


if __name__ == '__main__':
    with DatabaseQuery(r"database.db") as dbq:

        create_users_table = """
        CREATE TABLE IF NOT EXISTS Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        DateAccountCreated Date,
        DateOfBirth DATE,
        Email TEXT NOT NULL UNIQUE,
        PasswordHash TEXT NOT NULL,
        Username TEXT NOT NULL
        )
        """

        create_friends_table= """
        CREATE TABLE IF NOT EXISTS FriendConnections(
        FriendConnectionID INTEGER PRIMARY KEY AUTOINCREMENT,
        SenderFriendID INTEGER,
        ReceiverFriendID INTEGER,
        AcceptedRequest BOOLEAN,
        ConnectionStartTime TIME,
        ConnectionStartDate DATE,
        FOREIGN KEY (SenderFriendID) REFERENCES Users (UserID),
        FOREIGN KEY (ReceiverFriendID) REFERENCES Users (UserID)
        )
        """

        create_channel_table = """
        CREATE TABLE IF NOT EXISTS Channels(
        ChannelID INTEGER PRIMARY KEY AUTOINCREMENT,
        ChannelOwnerID INTEGER, 
        ChannelName TEXT,
        ChannelCreatedTime TIME,
        ChannelCreatedDate DATE,
        FOREIGN KEY (ChannelOwnerID) REFERENCES Users (UserID)
        );"""

        create_message_table = """
        CREATE TABLE IF NOT EXISTS Message(
        MessageID INTEGER PRIMARY KEY AUTOINCREMENT,
        ParentChannelID INTEGER,
        ParentUserID INTEGER,
        MessageContent TEXT,
        SentTime TIME,
        SentDate DATE,
        FOREIGN KEY (ParentChannelID) REFERENCES Channels (ChannelID),
        FOREIGN KEY (ParentUserID) REFERENCES Users (UserID)
        
        )
        """
        create_user_channels_connection_table = """
        CREATE TABLE IF NOT EXISTS UserChannelConnections (
        UserChannelConnectionID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INT,
        ChannelID INT,
        ConnectionCreatedTime TIME,
        ConnectionCreatedDate DATE,
        FOREIGN KEY (UserID) REFERENCES Users (UserID),
        FOREIGN KEY (ChannelID) REFERENCES Channel (ChannelID)
        );
        """
        """
        dbq.execute_query(create_users_table)
        dbq.execute_query(create_channel_table)
        dbq.execute_query(create_message_table)
        dbq.execute_query(create_user_channels_connection_table)
        dbq.execute_query(create_friends_table)
        dbq.add_user("Alex", "adavicenko@gmail.com", "pass", datetime(2006,3,3).date())
        dbq.add_user("User", "user@gmail.com", "pass", datetime(2009,3,3).date())
        dbq.add_user("User123", "user123@gmail.com", "pass123", datetime(2000,3,3).date())
        dbq.add_user("User124", "user124@gmail.com", "pass123", datetime(2000,3,4).date())
        dbq.add_user("User125", "user125@gmail.com", "pass123", datetime(2000,3,5).date())
        dbq.add_user("User126", "user126@gmail.com", "pass123", datetime(2000,3,6).date())


        dbq.add_channel(1, "Channel 1")
        dbq.add_channel(2, "Channel 2")

        dbq.add_user_channel_connection(1, 1)
        dbq.add_user_channel_connection(1, 2)
        dbq.add_user_channel_connection(2, 2)
        dbq.add_user_channel_connection(2, 4)
        dbq.add_user_channel_connection(1, 5)
        """
        #get_user_channels(26)
        
        print(dbq.get_user_channels(5))
