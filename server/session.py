import copy
from typing import List, Dict, Any

class Message:
    def __init__(self, sender_id: int, name: str, text: str, time: str) -> None:
        
        self.sender_id = sender_id
        self.sender_name = name
        self.text = text
        self.time = time
        self.received_by: List[int] = []
    
    def to_json(self) -> Dict[str, Any]:
        return {
            'sender_id': self.sender_id,
            'name': self.sender_name,
            'text': self.text,
            'time': self.time
        }


class Session:
    def __init__(self) -> None:

        self.client_ids: List[int] = []

        #Client ID: List[Message Object]
        self.messages: Dict[int, List[Message]]= {}

    def get_new_messages(self, client_id: int) -> List[Message]:
        #Get all the messages for the specific client ID
        new_msgs: List[Message] = self.messages.get(client_id, [])
        
        
        if new_msgs:    
            #Clear all the messages that are about to be sent out
            self.messages[client_id] = []
        
            #logging.info(f"Message returned for ID: {client_id} MSG stack {self.messages}")

        return new_msgs
        
    def add_message(self, msg: Message) -> None:
        #impl database call

        for client_id in self.client_ids:
            if client_id != msg.sender_id:
                new_msgs = self.messages.get(client_id, []) + [copy.deepcopy(msg)]
                self.messages[client_id] = new_msgs
                #logging.info(f"Message added to stack for ID: {client_id} Current Message Stack: {self.messages}")

