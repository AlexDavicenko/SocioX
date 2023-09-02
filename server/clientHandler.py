import logging
import pickle
import copy
import time
from threading import Thread, Event
from typing import List, Dict, Any
from socket import socket
from controller import Controller

#Specifying path to communication protocol directory
import sys
sys.path.append('../')
from communication_protocol.communicationProtocol import send_bytes, listen_for_bytes
from communication_protocol.TCPMessages import *
sys.path.append('client/')

class ClientHandler():
    def __init__(self, client: socket, controller: Controller, ip: str, port: str, id: int) -> None:
        self.client = client
        self.controller = controller
        self.ip = ip
        self.port = port
        self.id = id
        self.close_event = Event()
        self.controller.client_ids.append(self.id)
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
                for msg in self.controller.get_new_messages(self.id):
                    logging.info(f"Sending message to {self.id, (self.ip, self.port)}: [{msg}]")
                    self.send_msg(msg)
                    
                    time.sleep(0.5)

            except (ConnectionRefusedError, ConnectionResetError):
                logging.error(f"[CLIENT DISCONNECTED]: {self.ip, self.port}")
                self.close_event.set()
            
    def listen_thread(self) -> None:
        while not self.close_event.is_set():
            try:
                msg = self.receive_msg()
                logging.info(f"Recieved message from {self.id, (self.ip, self.port)}: [{msg}]")


                #Checking for type
                if isinstance(msg, TextMessage):
                    msg.client_id = self.id
                    self.controller.add_message(msg)

                elif isinstance(msg, ConnectionClosed):
                    pass

                elif isinstance(msg, LoginAttempt):
                    self.controller.add_message_by_id(self.id, LoginResponse(
                        datetime.now(),
                        0,
                        True,
                        self.id,
                        msg.name
                    ))
                elif isinstance(msg, ChannelJoinRequest):
                    self.controller.add_message_by_id(self.id, ChannelAddResponse(
                        datetime.now(),
                        msg.client_id,
                        True,
                        msg.channel_id,
                        self.controller.channels[msg.channel_id]
                    ))

                elif isinstance(msg, ChannelCreateRequest):
                    self.controller.add_message_by_id(self.id, ChannelAddResponse(
                        datetime.now(),
                        msg.client_id,
                        True,
                        self.controller.channel_id_counter,
                        msg.channel_name
                    ))
                    self.controller.channels[self.controller.channel_id_counter] = msg.channel_name
                    self.controller.channel_id_counter += 1

            except (ConnectionResetError, ConnectionRefusedError, ConnectionAbortedError):
                logging.error(f"[CLIENT DISCONNECTED]: {self.ip, self.port}")
                self.close_event.set()

    def send_msg(self, msg: TCPMessage) -> None:
        send_bytes(self.client, pickle.dumps(msg))

    def receive_msg(self) -> TCPMessage:

        msg: TCPMessage = pickle.loads(listen_for_bytes(self.client))
        return msg
