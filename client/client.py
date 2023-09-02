import socket
import logging
import json
import sys
import time
from datetime import datetime
from threading import Thread, Event
from controller_protocol import Controller

import sys
sys.path.append('../')
from communication_protocol.communicationProtocol import send_bytes, listen_for_bytes
from communication_protocol.TCPMessages import *
sys.path.append('client/')
import pickle

class Client():
    def __init__(self, controller: Controller, offline_mode = False) -> None:
        self.controller = controller
        self.close_event = Event()
        
        self.PORT = 8080
        self.HOST = "192.168.0.73"
        
        if offline_mode: return
        self.server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_conn.connect((self.HOST, self.PORT))

    def user_input(self):
        while not self.close_event.is_set():
            try:
                outgoing_msgs =  self.controller.get_outgoing_msgs()
                if outgoing_msgs:
                    for msg in outgoing_msgs:
                        logging.info(f"[MESSAGE SENT] {msg}")
                        self.send_msg(msg)
                        time.sleep(0.05)
                else:
                    time.sleep(0.2)

            except Exception as e:
                logging.error(str(e))
                self.close_event.set()


    def server_messages(self):
        while not self.close_event.is_set():
            try:
                msg_from_server = self.receive_msg()
                logging.info(f"[MESSAGE RECEIVED] {msg_from_server}")

                if isinstance(msg_from_server, NewMessageNotif):
                    self.controller.recieve_incoming_msg(msg_from_server)

                elif isinstance(msg_from_server, LoginResponse):
                    if msg_from_server.success:
                        self.controller.login_approved(msg_from_server.client_id, msg_from_server.client_username)
                
                elif isinstance(msg_from_server, ChannelAddResponse):
                    if msg_from_server.success:
                        self.controller.add_channel(
                            msg_from_server.channel_id,
                            msg_from_server.channel_name
                        )

            except (ConnectionResetError, ConnectionAbortedError) as e:
                logging.error(e)
                self.close_event.set()

    def receive_msg(self):
        msg = pickle.loads(listen_for_bytes(self.server_conn))
        return msg


    def send_msg(self, msg: TCPMessage):
        send_bytes(self.server_conn, pickle.dumps(msg))


    
    def close(self):

        exit(0)
        self.server_conn.close()


    def start(self):

        #TODO: 
        #   split into different files and classes
        Thread(target=self.user_input, args=()).start()
        Thread(target=self.server_messages, args=()).start()
    
