import logging
import json
import copy
import time
from threading import Thread
from typing import List, Dict, Any
from ..communication_protocol.communicationProtocol import send_bytes, listen_for_bytes
from socket import socket
from session import Session, Message

class HandleClient():
    def __init__(self, client: socket, session: Session, ip: str, port: str, id: int) -> None:
        self.client = client
        self.session = session
        self.ip = ip
        self.port = port
        self.id = id
        self.is_active = True
        self.session.client_ids.append(self.id)
        try:
            Thread(target=self.broadcast_thread).start()
            Thread(target=self.listen_thread).start()

        except ConnectionResetError:
            logging.info(f"[CONNECTION CRASH] {ip, port}")
            

    
    def broadcast_thread(self) -> None:        
        while self.is_active:
            try:
                for msg in self.session.get_new_messages(self.id):
                    logging.info(f"Sending message to {self.id, (self.ip, self.port)}: [{msg.to_json()}]")
                    self.send_msg(msg)
                    time.sleep(0.5)

            except (ConnectionRefusedError, ConnectionResetError):
                logging.error(f"[CLIENT DISCONNECTED]: {self.ip, self.port}")
                is_active = False
            
    def listen_thread(self) -> None:
        while self.is_active:
            try:
                #Check for type
                msg = self.receive()
                logging.info(f"Recieved message from {self.id, (self.ip, self.port)}: [{msg}]")
                self.session.add_message(Message(
                    self.id, 
                    msg['name'], 
                    msg['text'], 
                    msg['time']
                    ))


            except (ConnectionResetError, ConnectionRefusedError):
                logging.error(f"[CLIENT DISCONNECTED]: {self.ip, self.port}")
                is_active = False

    def send_msg(self, msg: Message) -> None:
        self.send_json(msg.to_json())

    def send_json(self, data: Dict[str, Any]) -> None:
        send_bytes(self.client, bytes(json.dumps(data), encoding="utf-8"))

    def receive(self) -> Dict[str, Any]:
        data: Dict[str, Any] = json.loads(listen_for_bytes(self.client))
        return data
