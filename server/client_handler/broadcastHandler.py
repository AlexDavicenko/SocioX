import pickle
import logging
import time
from threading import Event
from socket import socket
from controller import Controller

import sys; sys.path.append('../')

from communication_protocol.communicationProtocol import send_bytes
from communication_protocol.TCPMessages import *


class BroadcastHandler:
    def __init__(self, client: socket, close_event: Event, controller: Controller, client_id: int) -> None:
        self.client = client
        self.close_event = close_event
        self.controller = controller
        self.client_id = client_id

    def broadcast_thread(self) -> None:        
        while not self.close_event.is_set():
            try:
                msgs = self.controller.get_new_messages(self.client_id)
                if msgs:
                    for msg in msgs:
                        logging.info(f"Sending message to {self.client_id}: [{msg}]")
                    self.send_msg(msgs)
            
                
                time.sleep(0.05)
            except (ConnectionRefusedError, ConnectionResetError):
                logging.error(f"[CLIENT DISCONNECTED]: {self.client_id}")
                self.close_event.set()
            
    

    def send_msg(self, msg: TCPMessage) -> None:
        send_bytes(self.client, pickle.dumps(msg))