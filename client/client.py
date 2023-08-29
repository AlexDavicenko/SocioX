import socket
import logging
import json
import sys
import time
from datetime import datetime
from threading import Thread
from controller_protocol import Controller

import sys
sys.path.append('../')
from communication_protocol.communicationProtocol import send_bytes, listen_for_bytes
from communication_protocol.messagesTCP import *
sys.path.append('client/')
import pickle


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename='client.log',
)


class Client():
    def __init__(self, controller: Controller, name, offline_mode = False) -> None:
        self.controller = controller
        self.name = name
        
        self.PORT = 8080
        self.HOST = "192.168.0.73"
        self.close = False
        if offline_mode: return
        self.server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_conn.connect((self.HOST, self.PORT))


    def start(self):

        #TODO: 
        #   split into different files and classes
        Thread(target=self.user_input, args=()).start()
        Thread(target=self.server_messages, args=()).start()
    
    def user_input(self):
        while not self.close:
            try:
                outgoing_msgs =  self.controller.get_outgoing_msgs()
                if outgoing_msgs:
                    for msg in outgoing_msgs:
                        print("Message sent")
                        self.send_msg(msg)
                        time.sleep(0.05)
                time.sleep(0.5)

            except Exception as e:
                logging.error(str(e))
                self.close = True


    def server_messages(self):
    
        while not self.close:
            print('listen for bytes loop')
            try:
                msg_from_server = self.receive_msg()
                if isinstance(msg_from_server, NewMessageNotif):
                    self.controller.recieve_incoming_msg(msg_from_server)

            except ConnectionResetError:
                self.close = True

    def receive_msg(self):
        msg = pickle.loads(listen_for_bytes(self.server_conn))
        print(msg)
        #data = json.loads(listen_for_bytes(self.client))
        return msg


    def send_msg(self, msg: TCPMessage):
        try:
            send_bytes(self.server_conn, pickle.dumps(msg))
        except Exception as e:
            print(e)
    
        print("bytes sent")
        #self.send_json(
        #    {
        #        "name": self.name,
        #        "time": datetime.now().strftime('%H:%M:%S'),
        #        "text" : msg
        #    }
        #)

    def send_json(self, data):
        send_bytes(self.server_conn, bytes(json.dumps(data), encoding="utf-8"))
