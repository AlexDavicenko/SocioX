import logging
import pickle
import copy
import time
from threading import Thread, Event
from typing import List, Dict, Any
from socket import socket
from session import Session

#Specifying path to communication protocol directory
import sys
sys.path.append('../')
from communication_protocol.communicationProtocol import send_bytes, listen_for_bytes
from communication_protocol.messagesTCP import *
sys.path.append('client/')

class ClientHandler():
    def __init__(self, client: socket, session: Session, ip: str, port: str, id: int) -> None:
        self.client = client
        self.session = session
        self.ip = ip
        self.port = port
        self.id = id
        self.close_event = Event()
        self.session.client_ids.append(self.id)
        try:
            Thread(target=self.broadcast_thread).start()
            Thread(target=self.listen_thread).start()
            

        except ConnectionResetError:
            logging.info(f"[CONNECTION CRASH] {ip, port}")
            
    
    def close(self) -> None:
        self.client.close()
        self.close_event.set()
    
    def broadcast_thread(self) -> None:        
        while not self.close_event.is_set():
            try:
                for msg in self.session.get_new_messages(self.id):
                    if isinstance(msg, NewMessageNotif):
                        logging.info(f"Sending message to {self.id, (self.ip, self.port)}: [{msg}]")
                        self.send_msg(msg)
                    time.sleep(0.5)

            except (ConnectionRefusedError, ConnectionResetError):
                logging.error(f"[CLIENT DISCONNECTED]: {self.ip, self.port}")
                self.close_event.set()
            
    def listen_thread(self) -> None:
        while not self.close_event.is_set():
            try:
                #Check for type
                msg = self.receive_msg()
                logging.info(f"Recieved message from {self.id, (self.ip, self.port)}: [{msg}]")

                if isinstance(msg, ClientMessage):
                    msg.client_id = self.id
                    self.session.add_message(msg)

                elif isinstance(msg, ConnectionClosed):
                    pass

            except (ConnectionResetError, ConnectionRefusedError, ConnectionAbortedError):
                logging.error(f"[CLIENT DISCONNECTED]: {self.ip, self.port}")
                self.close_event.set()

    def send_msg(self, msg: TCPMessage) -> None:
        send_bytes(self. client, pickle.dumps(msg))

    def receive_msg(self) -> TCPMessage:

        msg = pickle.loads(listen_for_bytes(self.client))
        return msg
