import socket
import logging
import sys
import time
from threading import Thread, Event
from controller import Controller

import sys
sys.path.append('../')
from communication_protocol.communicationProtocol import TransmissionHandler
from communication_protocol.TCPMessages import *
sys.path.append('client/')
import pickle

class Client():
    def __init__(self, controller: Controller) -> None:
        self.controller = controller
        self.close_event = Event()
        
        self.PORT = 8080
        self.HOST = "192.168.0.73"
        self.server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_conn.connect((self.HOST, self.PORT))
        self.transmission_handler = TransmissionHandler(self.server_conn, False, self.close_event)
        self.transmission_handler.start()
        logging.info(f"Connected to server {self.HOST, self.PORT}")


    def user_input(self):
        while not self.close_event.is_set():
            try:
                msgs =  self.controller.get_outgoing_msgs()
                if msgs:
                    for msg in msgs:
                        logging.info(f"[MESSAGE SENT] {msg}")
                    self.send_msg(msgs)
                    time.sleep(0.05)
                else:
                    time.sleep(0.05)

            except Exception as e:
                logging.error(str(e))
                self.close_event.set()


    def server_messages(self):
        while not self.close_event.is_set():
            try:
                msgs = self.receive_msg()
                for msg in msgs:                  
                    logging.info(f"[MESSAGE RECEIVED] {msg}")

                    match msg:
                        case NewMessageNotif():
                            self.controller.recieve_incoming_msg(msg)
                        case LoginResponse():
                            if msg.success:
                                self.controller.login_approved(
                                    msg.user_id,
                                    msg.username, 
                                    msg.firstname, 
                                    msg.lastname, 
                                    msg.email, 
                                    msg.dob, 
                                    msg.account_created)
                            else:
                                self.controller.login_failed(msg.error_decription)
                        case ChannelCreateResponse():
                            if msg.success:
                                self.controller.create_channel(
                                    msg.channel_id,
                                    msg.channel_name
                                )
                        case ChannelJoinResponse():
                            if msg.success:
                                self.controller.join_channel(
                                    msg.channel_id,
                                    msg.channel_name
                                )
                        case ChannelLeaveNotif():
                            self.controller.user_left_channel_update(msg.channel_id, msg.username)
                        case UserJoinNotif():
                            self.controller.user_join_channel_update(
                                msg.channel_id, 
                                msg.username, 
                                msg.firstname, 
                                msg.lastname)
                        case SearchReponse():
                            self.controller.search_response(msg.response_data)
                        case FriendRequestNotif():
                            self.controller.friend_request_recieved(msg.username, msg.firstname, msg.lastname)
                        case FriendRemoval():
                            self.controller.remove_friend_notif(msg.username)
                        case FriendRequestDecision():
                            self.controller.friend_request_decision(msg.username, msg.success)
                        case FriendStatusNotif():
                            self.controller.friend_status_notif(
                                msg.username, 
                                msg.firstname, 
                                msg.lastname, 
                                msg.decision)
                        case SignUpResponse():
                            self.controller.signup_response(msg.success, msg.error_decription)
                        case SignUpConfirmation():
                            self.controller.signup_confirmation(msg.success, msg.user_id)
                        case _:
                            pass

            except (ConnectionResetError, ConnectionAbortedError) as e:
                logging.error(e)
                self.close_event.set()

    def receive_msg(self):
        msg = pickle.loads(self.transmission_handler.listen_for_bytes())
        return msg


    def send_msg(self, msg: TCPMessage):
        self.transmission_handler.send_bytes(pickle.dumps(msg))


    
    def close(self):
        self.server_conn.close()


    def start(self):
        Thread(target=self.user_input, args=()).start()
        Thread(target=self.server_messages, args=()).start()
    
