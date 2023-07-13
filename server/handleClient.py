from threading import Thread
import logging
import json
from communicationProtocol import send_bytes, listen_for_bytes

class HandleClient():
    def __init__(self, client, session, ip, port, id) -> None:
        self.client = client
        self.session = session
        self.ip = ip
        self.port = port
        self.id = id
        
        self.session.client_ids.append(self.id)
        try:
            Thread(target=self.broadcast_thread).start()
            Thread(target=self.listen_thread).start()

        except ConnectionResetError:
            logging.info(f"[CONNECTION CRASH] {ip, port}")
            
    
    
    def broadcast_thread(self):        
        is_active = True
        while is_active:
            try:
                for msg in self.session.get_new_messages(self.id):
                    print(msg)
                    self.send_msg(msg)
            except (ConnectionRefusedError, ConnectionResetError):
                is_active = False
            
    def listen_thread(self):
        is_active = True
        while is_active:
            try:
                #Check for type
                msg = self.receive()
                self.session.add_message(Message(self.id, msg['name'], msg['text'], msg['time']))

                


            except (ConnectionResetError, ConnectionRefusedError):
                logging.info(f"[CLIENT DISCONNECTED]: {self.ip, self.port}")
                is_active = False

    def send_msg(self, msg):
        self.send_json(msg.to_json())

    def send_json(self, data):
        send_bytes(self.client, bytes(json.dumps(data), encoding="utf-8"))

    def receive(self):
        data = json.loads(listen_for_bytes(self.client))
        return data


class Message:
    def __init__(self, sender_id, name, text, time) -> None:
        
        self.sender_id = sender_id
        self.sender_name = name
        self.text = text
        self.time = time
        self.received_by = []
    
    def to_json(self):
        return {
            'sender_id': self.sender_id,
            'name': self.sender_name,
            'text': self.text,
            'time': self.time
        }

class Session:
    def __init__(self) -> None:

        self.client_ids = []

        #Client ID: Message Object
        self.messages = {}

    def get_new_messages(self, client_id):
        new_msgs = self.messages.get(client_id, [])

        #for m in new_msgs:
            #m.received_by.append(client_id)
        
        self.messages[client_id] = []
        if new_msgs:
            for i in new_msgs:
                print(i.to_json())
        return new_msgs
        
    def add_message(self, msg):
        #impl database call

        for client_id in self.client_ids:
            if client_id != msg.sender_id:
                new_msgs = self.messages.get(client_id, []) + [msg]
                self.messages[client_id] = new_msgs
        
