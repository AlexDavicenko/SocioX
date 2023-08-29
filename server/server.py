
import logging
import socket
from threading import Thread, Event
from typing import List


from clientHandler import ClientHandler
from session import Session

class Server:
    def __init__(self, port: int) -> None:
        
        self.session = Session()
        self.close_event = Event()

        self.threads = 0
        self.current_clients: List[ClientHandler] = []
        self.id_counter = 0
        
        self.PORT = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.HOST = socket.gethostbyname(socket.gethostname())
        
        print(f"Running on: {(self.HOST,self.PORT)}")
        self.server.bind((self.HOST, self.PORT))
        self.server.listen()


    def start(self) -> None:
    
        Thread(target=self.accept_clients).start()
        self.listen_for_close()
        
  
    def accept_clients(self):
        while not self.close_event.is_set():
            try:
                client, address = self.server.accept()
                ip, port = str(address[0]), str(address[1])
                self.threads += 1
                self.id_counter += 1
                logging.info(f"[CLIENT CONNECTED] {ip,port}")
                client = ClientHandler(client, self.session, ip, port, self.id_counter)
                self.current_clients.append(client)
            except socket.error as e:
                print(e)


    def listen_for_close(self):
        
        while not self.close_event.is_set():
            console_msg = input()
            if console_msg == 'e':
                for client in self.current_clients:
                    client.close()
                self.server.close()
                self.close_event.set()




def main() -> None:

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename='server.log',
    )
    Server(8080).start()
        
if __name__ == "__main__":
    main()

