from socket import socket

WORD_LENGTH = 64

def send_bytes(connection: socket, data: bytes):
    header = str(f"{len(data):<{WORD_LENGTH}}").encode()
    
    connection.send(header)
    connection.send(data)

def listen_for_bytes(connection: socket):
    full_data = b""
    
    new_transmission = True
    while True:
        data = connection.recv(WORD_LENGTH)
        if new_transmission:
            #The int cast crashes often
            data_length = int(data[:WORD_LENGTH])
            new_transmission = False

        full_data += data


        if len(full_data)-WORD_LENGTH == data_length:
            return full_data[WORD_LENGTH:]

