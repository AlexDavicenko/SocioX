
import os
import pickle
import logging
from threading import Event
from socket import socket
from controller import Controller

import sys; sys.path.append('../')

from communication_protocol.communicationProtocol import TransmissionHandler
from communication_protocol.TCPMessages import *


class ListenHandler:
    def __init__(self, transmission_handler: TransmissionHandler, controller: Controller, client_id) -> None:
        self.transmission_handler = transmission_handler
        self.controller = controller
        self.client_id = client_id
        self.close_event = transmission_handler.close_event
        
    def listen_thread(self) -> None:
        while not self.close_event.is_set():
            try:
                msgs = self.receive_msg()
                for msg in msgs:
                    logging.info(f"Recieved message from {self.client_id}: [{msg}]")

                    self.controller.handle_message(msg, self.client_id)

            except (ConnectionResetError, ConnectionRefusedError, ConnectionAbortedError):
                logging.error(f"[CLIENT DISCONNECTED]: {self.client_id}")
                self.close_event.set()

    def receive_msg(self) -> TCPMessage:

        msg: TCPMessage = pickle.loads(self.transmission_handler.listen_for_bytes())
        return msg