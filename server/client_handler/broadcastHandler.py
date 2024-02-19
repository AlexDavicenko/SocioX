import pickle
import logging
import time
from controller import Controller

import sys; sys.path.append('../')

from communication_protocol.communicationProtocol import TransmissionHandler
from communication_protocol.TCPMessages import *


class BroadcastHandler:
    def __init__(self, transmission_handler: TransmissionHandler, controller: Controller, client_id: int) -> None:
        self.transmission_handler = transmission_handler
        self.close_event = transmission_handler.close_event
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
        self.transmission_handler.send_bytes(pickle.dumps(msg))