
import logging

import socket
from handleClient import HandleClient
from session import Session

class Server:
    def __init__(self, port: int) -> None:
        self.threads = 0
        self.id_counter = 0
        self.session = Session()
        self.PORT = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.HOST = socket.gethostbyname(socket.gethostname())
        print(f"Running on: {(self.HOST,self.PORT)}")

        self.server.bind((self.HOST, self.PORT))
        self.server.listen()

    def start(self) -> None:
        while True:
            client, address = self.server.accept()
            ip, port = str(address[0]), str(address[1])
            self.threads += 1
            self.id_counter += 1
            logging.info(f"[CLIENT CONNECTED] {ip,port}")

            HandleClient(client, self.session, ip, port, self.id_counter)
  


def main() -> None:

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename='server.log',
    )
    
    Server(8000).start()

if __name__ == "__main__":
    main()

