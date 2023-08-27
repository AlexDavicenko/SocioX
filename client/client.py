import socket
import logging
import json
import sys
from datetime import datetime
import time
from threading import Thread
from ..communication_protocol.communicationProtocol import send_bytes, listen_for_bytes


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename='client.log',
)


class Client():
    def __init__(self, app, name) -> None:
        self.app = app
        self.name = name

        self.PORT = 8000
        self.HOST = "127.0.1.1"
        self.close = False
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.HOST, self.PORT))


    def start(self):
        Thread(target=self.user_input, args=()).start()
        Thread(target=self.server_messages, args=()).start()
        pass

    def user_input(self):
        while not self.close:
            try:
                if self.app.messages_to_send:
                    msg = self.app.messages_to_send.pop()
                    print(msg)
                    self.send_msg(msg)
                time.sleep(0.5)

            except Exception as e:
                logging.error(str(e))
                self.close = True


    def server_messages(self):
    
        while not self.close:
            try:
                server_msg = self.receive()
                self.app.message_box_frame.add_message(
                    server_msg['name'],
                    server_msg['time'],
                    server_msg['text']
                )
            except ConnectionResetError:
                self.close = True

    def receive(self):
        data = json.loads(listen_for_bytes(self.client))
        return data


    def send_msg(self, msg):
        self.send_json(
            {
                "name": self.name,
                "time": datetime.now().strftime('%H:%M:%S'),
                "text" : msg
            }
        )

    def send_json(self, data):
        send_bytes(self.client, bytes(json.dumps(data), encoding="utf-8"))



def main():
    Client().start()


if __name__ == "__main__":
    main()
