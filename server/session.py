import copy
import logging
from typing import List, Dict, Any

import datetime
import sys
sys.path.append('../')
from communication_protocol.TCPMessages import *
sys.path.append('client/')


#Temporary before DB conn



class Session:
    def __init__(self) -> None:

        self.client_ids: List[int] = []
        #temp
        # ID: Name
        self.channels: Dict[int, str] =  {}
        self.channel_id_counter = 0

        #Client ID: List[Message Object]
        self.messages: Dict[int, List[TCPMessage]]= {}

    def get_new_messages(self, client_id: int) -> List[TCPMessage]:
        #Get all the messages for the specific client ID
        new_msgs: List[TCPMessage] = self.messages.get(client_id, [])
        
        
        if new_msgs:    
            #Clear all the messages that are about to be sent out
            self.messages[client_id] = []
        
            #logging.info(f"Message returned for ID: {client_id} MSG stack {self.messages}")

        return new_msgs
    
    def add_message_by_id(self, client_id: int, msg: TCPMessage):
        new_msgs = self.messages.get(client_id, []) + [msg] 
        self.messages[client_id] = new_msgs

        
    def add_message(self, msg: TextMessage) -> None:
        #impl database call
        
        if isinstance(msg, TextMessage):
            
            for client_id in self.client_ids:
                #Determine who needs to be notified about the message
                if client_id != msg.client_id:
                    
                    self.add_message_by_id(client_id, NewMessageNotif(
                        datetime.now(),
                        msg.channel_id,
                        msg.time_sent,
                        msg.client_id,
                        msg.text
                    ))

                    logging.info(f"Message added to stack for ID: {client_id} Current Message Stack: {self.messages}")

    