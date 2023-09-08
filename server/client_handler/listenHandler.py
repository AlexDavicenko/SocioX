
import os
import pickle
import logging
from threading import Event
from socket import socket
from controller import Controller

import sys; sys.path.append('../')

from communication_protocol.communicationProtocol import listen_for_bytes
from communication_protocol.TCPMessages import *


class ListenHandler:
    def __init__(self, client: socket, close_event: Event, controller: Controller, client_id) -> None:
        self.client = client
        self.close_event = close_event
        self.controller = controller
        self.client_id = client_id

    def listen_thread(self) -> None:
        while not self.close_event.is_set():
            try:
                msg = self.receive_msg()
                logging.info(f"Recieved message from {self.client_id}: [{msg}]")

                self.controller.handle_message(msg, self.client_id)
                
            except (ConnectionResetError, ConnectionRefusedError, ConnectionAbortedError):
                logging.error(f"[CLIENT DISCONNECTED]: {self.client_id}")
                self.close_event.set()

    def receive_msg(self) -> TCPMessage:

        msg: TCPMessage = pickle.loads(listen_for_bytes(self.client))
        return msg