from database.mySQLInterface import MySQLConnection
from database.graphDBInterface import GraphDBConnection

def reset_database(db_name, gdb_name):
    with MySQLConnection(db_name) as db:

        db.delete_database()
        db.create_database()
        db.create_table("Users", 
            """
            CREATE TABLE Users (
            UserID int(11) NOT NULL AUTO_INCREMENT,
            Username varchar(20) NOT NULL,
            Firstname varchar(20),
            Lastname varchar(20),
            Email varchar(50) NOT NULL,
            Region varchar(20),
            DateOfBirth datetime,
            DateAccountCreated datetime,
            PasswordSalt varchar(24),
            PasswordHash varchar(72),
            PRIMARY KEY (UserID),
            UNIQUE (Username)
            ) 
            """
        )
        db.create_table("Channels", 
            """
            CREATE TABLE Channels (
            ChannelID int(11) NOT NULL AUTO_INCREMENT,
            OwnerID int(10) NOT NULL,
            ChannelName varchar(20) NOT NULL,
            DateCreated datetime,
            PRIMARY KEY (ChannelID),
            FOREIGN KEY (OwnerID) REFERENCES Users(UserID)
            ) 
            """
        )

        db.create_table("Messages", 
            """
            CREATE TABLE Messages (
            MessageID int(11) NOT NULL AUTO_INCREMENT,
            SenderID int(11) NOT NULL,
            ChannelID int(11) NOT NULL,
            Content TEXT,
            DateSent datetime,
            PRIMARY KEY (MessageID),
            FOREIGN KEY (SenderID) REFERENCES Users(UserID),
            FOREIGN KEY (ChannelID) REFERENCES Channels(ChannelID)
            ) 
            """
        )
            

        db.create_table("UserChannelConnection", 
            """
            CREATE TABLE UserChannelConnection (
            UserChannelConnectionID int(11) NOT NULL AUTO_INCREMENT,
            UserID int(11) NOT NULL,
            ChannelID int(11) NOT NULL,
            DateUserAdded datetime,
            PRIMARY KEY (UserChannelConnectionID),
            FOREIGN KEY (UserID) REFERENCES Users(UserID),
            FOREIGN KEY (ChannelID) REFERENCES Channels(ChannelID)
            ) 
            """
        )

        db.create_table("FriendConnections", 
            """
            CREATE TABLE FriendConnections (
            FriendConnectionID int(11) NOT NULL AUTO_INCREMENT,
            FriendRequestSenderID int(11) NOT NULL,
            FriendRequestReceiverID int(11) NOT NULL,
            DateRequestSent datetime NOT NULL,
            DateRequestAccepted datetime,
            PRIMARY KEY (FriendConnectionID),
            FOREIGN KEY (FriendRequestSenderID) REFERENCES Users(UserID),
            FOREIGN KEY (FriendRequestReceiverID) REFERENCES Users(UserID)
            ) 
            """
        )
        db.create_table("MessageEditLog", 
            """
            CREATE TABLE MessageEditLog (
            MessageEditID int(11) NOT NULL AUTO_INCREMENT,
            MessageID int(11) NOT NULL,
            DateEdited datetime NOT NULL,
            Content TEXT,
            PRIMARY KEY (MessageEditID),
            FOREIGN KEY (MessageID) REFERENCES Messages(MessageID)
            ) 
            """
            )



    with GraphDBConnection(gdb_name) as gdb:
        gdb.reset()