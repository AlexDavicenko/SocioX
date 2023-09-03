import logging
from threading import Thread, Event
from typing import List, Dict, Any
from socket import socket
from controller import Controller

from client_handler.broadcastHandler import BroadcastHandler
from client_handler.listenHandler import ListenHandler

class ClientHandler():
    def __init__(self, client: socket, controller: Controller, ip: str, port: str, client_id: int) -> None:
        self.client = client
        self.controller = controller
        self.ip = ip
        self.port = port

        self.client_id = client_id
        self.controller.client_ids.append(client_id)

        self.close_event = Event()
        
        try:
            self.broadcast_handler = BroadcastHandler(self.client, self.close_event, self.controller, self.client_id)
            self.listen_handler = ListenHandler(self.client, self.close_event, self.controller, self.client_id)

            Thread(target=self.broadcast_handler.broadcast_thread).start()
            Thread(target=self.listen_handler.listen_thread).start()

        except ConnectionResetError:
            logging.info(f"[CONNECTION CRASH] {ip, port}")
            
    
    def close(self) -> None:
        self.client.close()
        self.close_event.set()
    
    

    
