from socket import socket
from threading import Event
WORD_LENGTH = 64

def send_bytes(connection: socket, data: bytes) -> None:
    header = str(f"{len(data):<{WORD_LENGTH}}").encode()
    connection.send(header)
    connection.send(data)

def listen_for_bytes(connection: socket, close_event: Event = Event()) -> bytes:
    full_data = b""
    
    new_transmission = True
    while not close_event.is_set():
        print("This goofy loop")
        data = connection.recv(WORD_LENGTH)
        if new_transmission:
            #The int cast crashes often
            if data[:WORD_LENGTH]:
                data_length = int(data[:WORD_LENGTH])
                new_transmission = False

        full_data += data


        if len(full_data)-WORD_LENGTH == data_length:
            return full_data[WORD_LENGTH:]

