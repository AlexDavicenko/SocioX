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
        #self.server_conn.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 102400)
        self.server_conn.connect((self.HOST, self.PORT))

        logging.info(f"Connected to server {self.HOST, self.PORT}")

    def user_input(self):
        while not self.close_event.is_set():
            try:
                outgoing_msgs =  self.controller.get_outgoing_msgs()
                if outgoing_msgs:
                    for msg in outgoing_msgs:
                        logging.info(f"[MESSAGE SENT] {msg}")
                        self.send_msg(msg)
                        time.sleep(0.001)
                else:
                    time.sleep(0.001)

            except Exception as e:
                logging.error(str(e))
                self.close_event.set()


    def server_messages(self):
        while not self.close_event.is_set():
            try:

                msgs = self.receive_msg()
                for msg in msgs:                  
                    logging.info(f"[MESSAGE RECEIVED] {msg}")

                    if isinstance(msg, NewMessageNotif):
                        self.controller.recieve_incoming_msg(msg)

                    elif isinstance(msg, LoginResponse):
                        if msg.success:
                            self.controller.login_approved()
                    
                    elif isinstance(msg, ChannelAddResponse):
                        if msg.success:
                            self.controller.add_channel(
                                msg.channel_id,
                                msg.channel_name
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
        self.server_conn.close()


    def start(self):

        #TODO: 
        #   split into different files and classes
        Thread(target=self.user_input, args=()).start()
        Thread(target=self.server_messages, args=()).start()
    
