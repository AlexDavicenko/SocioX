from socket import socket
from threading import Event
from random import sample, randint
from time import perf_counter
import pickle
from typing import Tuple

def gcd(x, y) -> int:
    while x != 0:
        x, y = y % x, x
    return y

def extended_gcd(x: int, y: int) -> Tuple[int, int, int]:
    prev_u = 1
    prev_v = 0
    u = 0
    v = 1

    while y != 0:
        q = x // y
        x, y = y, x % y

        u_new = prev_u - q * u
        v_new = prev_v - q * v


        prev_u, prev_v = u, v
        u, v = u_new, v_new

    return x, prev_u, prev_v


def generate_keys_fast(p, q) -> Tuple[int, int]:
    N = p*q 

    # phi(x) evaluated at N
    phiN = (p-1)*(q-1)

    e = 0 
    while True:
        potential_e = randint(2, phiN-1)

        if gcd(phiN,potential_e) == 1:
            e = potential_e
            break
    assert e != 0

    public_key = (e, N)    
  
    _, _, y = extended_gcd(phiN, e)

    private_key = (y, N)


    return public_key, private_key


class TransmissionHandler:
    WORD_LENGTH = 256
    PRIMES_FILE_PATH = "..\communication_protocol\primes_for_rsa.txt"
    def __init__(self, connection: socket, initiator: bool, close_event: Event = Event()) -> None:
        self.connection = connection
        self.initiator = initiator
        self.close_event = close_event

        self.my_public_key = None
        self.my_private_key = None
        self.their_public_key = None

    def start(self):
        if self.initiator:
            self.initiate_handshake()
        else:
            self.recieve_handshake()
    
    def initiate_handshake(self):
        p, q = self.get_2_primes()

        self.my_public_key, self.my_private_key = generate_keys_fast(p, q)
        self.send_bytes(pickle.dumps(self.my_public_key), encrypt=False)
        self.their_public_key = pickle.loads(self.listen_for_bytes(encrypted=False))

        print("Handshake complete")


    def recieve_handshake(self):
        self.their_public_key = pickle.loads(self.listen_for_bytes(encrypted=False))

        p, q = self.get_2_primes()
    
        self.my_public_key, self.my_private_key = generate_keys_fast(p, q)
        self.send_bytes(pickle.dumps(self.my_public_key), encrypt=False)

        print("Handshake complete")

    def encrypt(self, plain_text: bytes, public_key) -> bytes:
        e, N = public_key

        plain_int = int.from_bytes(plain_text, byteorder= 'little')
        cypher_int = pow(plain_int, e, N)

        cypher_text = cypher_int.to_bytes(self.WORD_LENGTH, byteorder="little")

        return cypher_text

    def decrypt(self, cypher_text: bytes, private_key) -> bytes:
        d, N = private_key

        cypher_int = int.from_bytes(cypher_text, byteorder = 'little')
        plain_int = pow(cypher_int, d, N)
        
        plain_text = plain_int.to_bytes(self.WORD_LENGTH, byteorder = "little")

        return plain_text

    def listen_for_bytes(self, encrypted: bool = True) -> bytes:

        full_data = b""

        
        new_transmission = True
        while not self.close_event.is_set():

            data = self.connection.recv(self.WORD_LENGTH)

            #Decrypt if encryption is set up
            if encrypted:
                data = self.decrypt(data, self.my_private_key)
            
            if new_transmission:
                if data[:self.WORD_LENGTH]:
                    data_length = int(data[:self.WORD_LENGTH])
                    new_transmission = False
            else:
                full_data += data
            
            if len(full_data) >= data_length:
                return full_data[:data_length]
            

    def send_bytes(self, data: bytes, encrypt: bool = True) -> None:

        #Cite
        print(len(data)) 
        header = str(f"{len(data):<{self.WORD_LENGTH}}").encode()
        if encrypt:
            encrypted_header = self.encrypt(header, self.their_public_key)
            self.connection.send(encrypted_header)

            echunks = []
            for i in range(0, len(data), self.WORD_LENGTH):
                chunk = data[i:i+self.WORD_LENGTH]
                encrypted_chunk = self.encrypt(chunk, self.their_public_key)
                echunks.append(encrypted_chunk)

            encrpyted_data = b"".join(echunks)
            self.connection.send(encrpyted_data)

        else:
            self.connection.send(header)
            self.connection.send(data)


    def get_2_primes(self):
        with open(self.PRIMES_FILE_PATH, "r") as f:
            primes = f.read().splitlines()

            while True:
                #Ensure that the product of the primes is 2048 bits (pain </3)
                p, q = map(int, sample(primes, 2))
                prod_len = (p * q).bit_length()
                if prod_len == self.WORD_LENGTH*8:
                    return  p, q


    